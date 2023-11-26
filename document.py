
import cohere
import os
import hnswlib
import json
import uuid
from typing import List, Dict
from dotenv import load_dotenv
import numpy as np
from unstructured.partition.html import partition_html
from unstructured.chunking.title import chunk_by_title

load_dotenv()

# Access the API key
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)


class Documents:

    def __init__(self, source: str ):
        self.source = source
        self.docs = []
        self.docs_embs = []
        self.retrieve_top_k = 10
        self.rerank_top_k = 3
        self.load()
        self.embed()
        self.index()
    
    def load(self) -> None:

        print("Loading documents...")
        file_list = [file for file in os.listdir(self.source) if file.endswith(".txt")]

        for file_name in file_list:
            file_path = os.path.join(self.source, file_name)

            with open(file_path, 'r') as file:
                file_contents = file.read()
                file.seek(0)
                url = file.readline().strip()

                self.docs.append({
                    "url": url, 
                    "text": file_name
                })

    def embed(self):
        print("Embedding documents...")

        batch_size = 1
        self.docs_len = len(self.docs)

        for i in range(0, self.docs_len, batch_size):
            batch = self.docs[i : min(i + batch_size, self.docs_len)]
            texts = [item["text"] for item in batch]
            docs_embs_batch = co.embed(
		              texts=texts,model="embed-english-v3.0",input_type="search_document"
	 		).embeddings
            self.docs_embs.extend(docs_embs_batch)

        temp = np.array(self.docs_embs)
        return 
    
    def index(self) -> None:
        """
        Indexes the documents for efficient retrieval.
        """

        print("Indexing documents...")

        self.index = hnswlib.Index(space="ip", dim=1024)
        self.index.init_index(max_elements=self.docs_len, ef_construction=512, M=64)
        self.index.add_items(self.docs_embs, list(range(len(self.docs_embs))))

        print(f"Indexing complete with {self.index.get_current_count()} documents.")

    def retrieve(self, query: str) -> List[Dict[str, str]]:
        """
        Retrieves documents based on the given query.

        Parameters:
        query (str): The query to retrieve documents for.

        Returns:
        List[Dict[str, str]]: A list of dictionaries representing the retrieved  documents, with 'title', 'snippet', and 'url' keys.
        """

        docs_retrieved = []
        
        query_emb = co.embed(
                    texts=[query],
                    model="embed-english-v3.0",
                    input_type="search_query"
                    ).embeddings				    

        doc_ids = self.index.knn_query(query_emb, k=min(self.retrieve_top_k, self.docs_len))[0][0]

        docs_to_rerank = []
        for doc_id in doc_ids:
            docs_to_rerank.append(self.docs[doc_id]["text"])

        rerank_results = co.rerank(
            query=query,
            documents=docs_to_rerank,
            top_n=min(self.rerank_top_k, self.docs_len),
            model="rerank-english-v2.0",
        )

        doc_ids_reranked = []
        url = []
        for result in rerank_results:
            doc_ids_reranked.append(doc_ids[result.index])

        for doc_id in doc_ids_reranked:
            docs_retrieved.append(
                {
                    "text": self.docs[doc_id]["text"],
                    "url": self.docs[doc_id]["url"],
                }
            )

        return docs_retrieved

a = Documents("/Users/priyanshusharma/cohere-rag/test")
print(a.retrieve("hello"))