from app.retrieval.chunk_documents import build_document_chunks
from app.retrieval.vector_store import save_vector_index


def main():
    chunks = build_document_chunks()

    if not chunks:
        raise RuntimeError("No document chunks found. Check app/data/docs.")

    save_vector_index(chunks)

    print(f"Vector index built successfully with {len(chunks)} chunks.")


if __name__ == "__main__":
    main()