import uuid

import chromadb


class VectorStoreManager:
    def __init__(self, collection_name="document_qa"):
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path="./chroma_db")

        self.embedding_func = (
            chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
        try:
            # Try to get the existing collection first
            self.collection = self.client.get_collection(name=self.collection_name)
        except Exception:
            # If it doesn't exist, create it and attach the embedding function
            self.collection = self.client.create_collection(
                name=self.collection_name, embedding_function=self.embedding_func
            )

    def add_documents(self, chunks: list[dict]) -> None:
        self.collection.add(
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
            ids=[str(uuid.uuid4()) for _ in chunks],
        )

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        result = self.collection.query(query_texts=[query], n_results=top_k)

        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]

        return [
            {"text": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]
