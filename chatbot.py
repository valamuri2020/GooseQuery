from document import *


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

class Chatbot:
    def __init__(self, docs: Documents):
        self.docs = docs
        self.conversation_id = str(uuid.uuid4())

    def generate_response(self, message: str):
        """
        Generates a response to the user's message.

        Parameters:
        message (str): The user's message.

        Yields:
        Event: A response event generated by the chatbot.

        Returns:
        List[Dict[str, str]]: A list of dictionaries representing the retrieved documents.

        """

        # Generate search queries (if any)

        response = co.chat(model="command-nightly", message=message, search_queries_only=True)

        if response.search_queries:
            print("Retrieving information...")
            documents = self.retrieve_docs(response)

            response = co.chat(
                model="command-nightly", 
                message=message,
                documents=documents,
                conversation_id=self.conversation_id,
            )

            return response.text
        else:
            response = co.chat(
                model="command-nightly", 
                message=message, 
                conversation_id=self.conversation_id, 
            )

            return response.text

    def retrieve_docs(self, response) -> List[Dict[str, str]]:
        
        """
        Retrieves documents based on the search queries in the response.

        Parameters:
        response: The response object containing search queries.

        Returns:
        List[Dict[str, str]]: A list of dictionaries representing the retrieved documents.

        """
        queries = []
        for search_query in response.search_queries:
            queries.append(search_query["text"])

        # Retrieve documents for each query
        retrieved_docs = []
        for query in queries:
            retrieved_docs.extend(self.docs.retrieve(query))

        return retrieved_docs
    
# a = Documents("/Users/priyanshusharma/cohere-rag/test")
# chat = Chatbot(a)
# x = chat.generate_response("search 'hello world' inside documents")
# print(x)