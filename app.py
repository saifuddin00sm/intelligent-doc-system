from src.document_loader import DocumentProcessor
# from src.vector_store import VectorStoreManager
# from src.llm_generator import LLMGenerator
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from starlette.concurrency import run_in_threadpool
import shutil

app = FastAPI()


def save_file_sync(input_file_obj, output_path):
    with open(output_path, "wb") as buffer:
        shutil.copyfileobj(input_file_obj, buffer)


def main():
    document_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.post("/upload/")
    async def create_upload_file(file: UploadFile):
        output_path = Path("uploads") / file.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await file.seek(0)
        await run_in_threadpool(save_file_sync, file.file, output_path)

        print('output_path: ', output_path)

        document_chunks = document_processor.load_and_chunk_pdf(output_path)


        return {"filename": file.filename, "total_chunks": len(document_chunks)}

    # vector_store_manager = VectorStoreManager()

    # llm_generator = LLMGenerator()

    # document_chunks = document_processor.load_and_chunk_pdf("data/resume.pdf")
    # print(f"Successfully created {len(document_chunks)} chunks from the document.")

    # vector_store_manager.add_documents(document_chunks)

    # while True:
    #     user_input = input("Ask a question ('exit' to quit): ")
    #     if user_input.lower() in ["exit", "quit"]:
    #         print("Goodbye, see you soon!")
    #         break

    #     search_result = vector_store_manager.search(user_input)

    #     ai_generated_answer = llm_generator.generate_answer(user_input, search_result)

    #     print(ai_generated_answer)


main()
