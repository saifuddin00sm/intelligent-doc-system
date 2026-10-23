from src.document_loader import DocumentProcessor
from src.vector_store import VectorStoreManager
from src.llm_generator import LLMGenerator


def app():
    document_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    vector_store_manager = VectorStoreManager()

    llm_generator = LLMGenerator()

    document_chunks = document_processor.load_and_chunk_pdf("data/resume.pdf")
    print(f"Successfully created {len(document_chunks)} chunks from the document.")

    vector_store_manager.add_documents(document_chunks)

    while True:
        user_input = input("Ask a question ('exit' to quit): ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye, see you soon!")
            break

        search_result = vector_store_manager.search(user_input)

        ai_generated_answer = llm_generator.generate_answer(user_input, search_result)

        print(ai_generated_answer)


app()
