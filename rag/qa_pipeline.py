import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


class QAPipeline:
    def __init__(self, embedder, vector_store, llm_client,
                 rag_instruction_file="instructions/rag_instructions.txt",
                 agent_instruction_file="instructions/agent_instructions.txt"):
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm_client

        # Detect environment (default = local)
        env = os.getenv("ENV", "local").lower()
        if env == "prod":
            # Use paths relative to this Python file in production/server
            base_dir = Path(__file__).parent
            rag_path = base_dir / rag_instruction_file
            agent_path = base_dir / agent_instruction_file
        else:
            # Use current working directory for local dev
            rag_path = Path(rag_instruction_file)
            agent_path = Path(agent_instruction_file)

        self.rag_instructions = self._load_instruction(rag_path)
        self.agent_instructions = self._load_instruction(agent_path)
        self.instruction_text = self._combine_instructions()

    def _load_instruction(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            logging.warning(f"Instruction file {file_path} not found.")
            return ""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logging.error(f"Failed to load instruction file {file_path}: {e}")
            return ""

    def _combine_instructions(self) -> str:
        instructions = ""
        if self.agent_instructions:
            instructions += f"{self.agent_instructions}\n\n"
        if self.rag_instructions:
            instructions += f"{self.rag_instructions}"
        return instructions.strip()

    def answer(self, question: str, chat_history: list = None, k: int = 5) -> str:
        try:
            chat_context = ""
            if chat_history:
                for msg in chat_history:
                    role = "User" if msg["role"] == "user" else "Bot"
                    chat_context += f"{role}: {msg['content']}\n"

            retrieved_chunks = self.vector_store.search(question, k=k)

            # Handle case where vector search returned error message
            if len(retrieved_chunks) == 1 and retrieved_chunks[0].startswith("⚠️"):
                return retrieved_chunks[0]

            merged_by_header = {}
            for idx, chunk in enumerate(retrieved_chunks):
                if isinstance(chunk, dict) and "header" in chunk and "text" in chunk:
                    header = chunk["header"]
                    text = chunk["text"]
                    if header in merged_by_header:
                        merged_by_header[header] += " " + text
                    else:
                        merged_by_header[header] = text
                else:
                    merged_by_header[f"chunk_{idx}"] = str(chunk)

            context = "\n\n".join(merged_by_header.values())

            prompt = f"""
{self.instruction_text}
Conversation history:
{chat_context}
Context from documents:
{context}
User question:
{question}
Answer:
"""
            response = self.llm.ask(prompt)
            return response
        except Exception as e:
            logging.error(f"Error during answer generation: {e}")
            return "⚠️ Something went wrong while generating the answer. Please check your internet connection and try again."
