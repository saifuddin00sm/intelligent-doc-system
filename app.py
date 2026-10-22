from src.document_loader import DocumentProcessor


def app():
    document_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

    pdf_text = document_processor.load_and_chunk_pdf("data/resume.pdf")


    print(len(pdf_text))



app()