import ollama


class LLMGenerator:
    def __init__(self):
        self.model = "qwen2.5"

    def generate_answer(self, query: str, context: list[dict]) -> str:

        formatted_context = "\n\n".join(
            [f"Source {i + 1}: {chunk['text']}" for i, chunk in enumerate(context)]
        )
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Answer the user's question based ONLY on the provided context. If the answer cannot be found in the context, reply with 'I do not have enough information to answer that'.",
                    },
                    {
                        "role": "user",
                        "content": f"Context: {formatted_context}\n\nQuestion: {query}",
                    },
                ],
            )

            return response.message.content

        except Exception as e:
            return f"Error: The AI brain is currently unavailable. Please ensure Ollama is running.: {e}"
