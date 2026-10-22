from src.document_loader import DocumentProcessor
from src.vector_store import VectorStoreManager


def app():
    document_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    vector_store_manager = VectorStoreManager()

    document_chunks = document_processor.load_and_chunk_pdf("data/resume.pdf")
    print(f"Successfully created {len(document_chunks)} chunks from the document.")

    vector_store_manager.add_documents(document_chunks)

    while True:
        try:
            user_input = input("Ask a question ('exit' to quit): ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye, see you soon!")
                break

            search_result = vector_store_manager.search(user_input)

            for i, result in enumerate(search_result):
                print(
                    f"Result {i + 1} (Score: {result['distance']:.4f}):\n{result['text']}\n"
                )
        except RuntimeError as e:
            print("Something went wrong", e)


app()