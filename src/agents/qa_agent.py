from config import model
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
import streamlit as st 
from agents import  SearchAgent


            
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

class QAAgent:
    def __init__(self):
        
        self.model = model
        self.prompt = """You are a research assistant answering questions about academic papers. Use the following context from papers and chat history to provide accurate, specific answers.

        Previous conversation:
        {chat_history}

        Paper context:
        {context}

        Question: {question}

        Guidelines:
        1. Reference specific papers when making claims
        2. Use direct quotes when relevant
        3. Acknowledge if information isn't available in the provided context
        4. Maintain academic tone and precision
        """
        self.papers = None
        self.search_agent_response  = ""

    def solve(self, query):
        # Check if search has been performed
        if not os.path.exists("vdb_chunks"):
            st.warning("No papers loaded. Performing search first...")
            search_agent = SearchAgent()
            self.search_agent_response , self.papers = search_agent.solve(query)
            
        # Load vector store
        vdb_chunks = FAISS.load_local("vdb_chunks", embeddings, index_name="base_and_adjacent", allow_dangerous_deserialization=True)
        
        # Get chat history
        chat_history = st.session_state.get("chat_history", [])
        chat_history_text = "".join([f"{sender}: {msg}" for sender, msg in chat_history[-5:]])  # Last 5 messages
        
        # Get relevant chunks
        retrieved = vdb_chunks.as_retriever().get_relevant_documents(query)
        context = "".join([f"{doc.page_content}\n Source: {doc.metadata['source']}" for doc in retrieved])
        
        # Generate response
        full_prompt = self.prompt.format(
            chat_history=chat_history_text,
            context=context,
            question=query
        )
        
        response = self.model.generate_content(str(self.search_agent_response)  + full_prompt)
        return response.text , self.papers