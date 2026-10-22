from src.document_loader import DocumentProcessor
from src.vector_store import VectorStoreManager


def app():
    document_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    vector_store_manager = VectorStoreManager()

    # document_chunks = document_processor.load_and_chunk_pdf("data/resume.pdf")


    # vector_store_manager.add_documents(document_chunks)

    search_result = vector_store_manager.search("What is the portfolio link?")
    print(search_result)



app()