import os
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import DATA_DIR, EMBEDDING_MODEL

class DocumentRetriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = None
        self._initialize_corpus()

    def _initialize_corpus(self):
        index_path = "faiss_index"

        if os.path.exists(index_path):
            print("Loading existing FAISS index...")
            self.vector_store = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return

        print("Creating new FAISS index...")
        documents = []

        for md_file in DATA_DIR.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        rel_path = md_file.relative_to(DATA_DIR)
                        company_name = rel_path.parts[0].lower()
                        product_area = rel_path.parts[1]
                        name = md_file.name.lower()

                        documents.append(Document(
                            page_content=content,
                            metadata={
                                "source": str(rel_path),
                                "company": company_name,
                                "product_area": product_area,
                                "name": name
                            }
                        ))
            except Exception as e:
                print(f"Error reading {md_file}: {e}")

        if not documents:
            print("No documents found.")
            return

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        splits = splitter.split_documents(documents)

        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        self.vector_store.save_local(index_path)

        print(f"Saved FAISS index with {len(splits)} chunks.")

    def retrieve(self, company, issue, subject, top_k=3):
        if not self.vector_store:
            return [], [], False
        
        query = f"{company} {subject} {issue}"
        docs_and_scores = []
        fallback_triggered = False
        company_lower = str(company).strip().lower()

        if company_lower and company_lower != "none":
            docs_and_scores = self.vector_store.similarity_search_with_score(query, k=top_k, filter={"company": company_lower})

        if not docs_and_scores:
            fallback_triggered = True
            docs_and_scores = self.vector_store.similarity_search_with_score(query, k=top_k)

        documents = [doc.page_content for doc, score in docs_and_scores]
        scores = [float(score) for doc, score in docs_and_scores]

        return documents, scores, fallback_triggered

retriever = DocumentRetriever()
