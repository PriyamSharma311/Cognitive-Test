import os

# Modern LangChain imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_index():
    kb_path = "/Users/priyamsharma/Documents/Et Gen ai hackathon/Knowledge base"
    index_path = "embeddings/faiss_index"

    os.makedirs(index_path, exist_ok=True)

    texts = []

    # Load knowledge base text files
    for file in os.listdir(kb_path):
        if file.endswith(".txt"):
            with open(os.path.join(kb_path, file), "r", encoding="utf-8") as f:
                texts.append(f.read())

    if not texts:
        print("❌ No .txt files found in knowledge_base/")
        return

    print("✅ Knowledge base loaded")

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = splitter.split_text("\n".join(texts))

    print(f"✅ Created {len(docs)} text chunks")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Build FAISS index
    db = FAISS.from_texts(docs, embeddings)

    # Save index
    db.save_local(index_path)

    print("✅ FAISS index created")
    print("📁 embeddings/faiss_index/index.faiss")
    print("📁 embeddings/faiss_index/index.pkl")


if __name__ == "__main__":
    build_index()

