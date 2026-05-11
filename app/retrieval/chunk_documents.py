from pathlib import Path
from typing import Dict, List


DOCS_DIR = Path("app/data/docs")


def read_markdown_files(docs_dir: Path = DOCS_DIR) -> List[Dict[str, str]]:
    documents = []

    for file_path in docs_dir.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


def split_text_into_chunks(
    text: str,
    chunk_size: int = 700,
    overlap: int = 120,
) -> List[str]:
    clean_text = " ".join(text.split())

    if len(clean_text) <= chunk_size:
        return [clean_text]

    chunks = []
    start = 0

    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end]
        chunks.append(chunk)

        start = end - overlap

        if start < 0:
            start = 0

        if start >= len(clean_text):
            break

    return chunks


def build_document_chunks() -> List[Dict[str, str]]:
    documents = read_markdown_files()
    chunks = []

    for document in documents:
        source = document["source"]
        text = document["text"]

        split_chunks = split_text_into_chunks(text)

        for index, chunk_text in enumerate(split_chunks):
            chunks.append(
                {
                    "chunk_id": f"{source}_chunk_{index}",
                    "source": source,
                    "text": chunk_text,
                }
            )

    return chunks


if __name__ == "__main__":
    chunks = build_document_chunks()

    print(f"Created {len(chunks)} chunks.")
    for chunk in chunks:
        print(f"- {chunk['chunk_id']} from {chunk['source']}")