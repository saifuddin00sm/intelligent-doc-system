from pypdf import PdfReader
import os


class DocumentProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_and_chunk_pdf(self, pdf_path: str) -> list[dict]:
        """
        Load a PDF document and chunk it into smaller pieces.

        Args:
            pdf_path (str): The path to the PDF file.
        Returns:
            list[dict]: A list of chunks (dictionaries).
        """

        if not os.path.exists(pdf_path) or not pdf_path.lower().endswith(".pdf"):
            raise FileNotFoundError(f"The file '{pdf_path}' does not exist or is not a PDF.")

        reader = PdfReader(pdf_path)
        pages = reader.pages


        full_text = '\n'.join([page.extract_text() for page in pages]).replace("\n", " ")


        chunks = []
        for i in range(0, len(full_text), self.chunk_size - self.chunk_overlap):
            chunk = full_text[i : i + self.chunk_size]
            chunks.append({"text": chunk, "metadata": {"source": os.path.basename(pdf_path)}})


        return chunks
