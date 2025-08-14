import streamlit as st
from dotenv import load_dotenv #load_dotenv() allows us to use environment variables from a .env file
from PyPDF2 import PdfReader  
from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import htmlTemplates
from langchain.memory import ConversationBufferMemory

import os

load_dotenv()

#this function will return the pdf as a long single text
def get_pdf_text(pdf_docs):
    text=''
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
    
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text
    
    
    
def get_text_chunks(text):
    text_splitter=CharacterTextSplitter(
        separator="\n", 
        chunk_size=1000,  
        chunk_overlap=200,  
        length_function=len
    )
    
    chunks=text_splitter.split_text(text)
    
    return chunks
    
def get_vectorstore(text_chunks):
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain
    
    
def handle_user_input(user_question):
    response = st.session_state.conversation({
            "question": user_question,
            "chat_history": st.session_state.chat_history
        })
    st.write(response['answer'])
    
    
def main():
    load_dotenv()  # Load environment variables from .env file
    st.set_page_config(page_title="My Streamlit App", page_icon=":books:")
    
    st.write(htmlTemplates.css, unsafe_allow_html=True)
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None
    # Initialize the conversation state if it doesn't exist
    
    
    st.header("Welcome to My Streamlit App Chat with multiple PDFs")
    user_question=st.text_input("Ask a question about your PDFs:")

    if user_question:
        handle_user_input(user_question)
    
    

    with st.sidebar:
        st.subheader("Upload PDFs")
        pdf_docs=st.file_uploader(
            "Upload PDF files then process",accept_multiple_files=True)
        if st.button("Process PDFs"):
            #do everything inside this while spinning 
            with st.spinner("Processing PDFs..."):
                #get pdf text
                raw_text=get_pdf_text(pdf_docs)
                #st.write(raw_text)
                
                #get the text chunks
                text_chunks=get_text_chunks(raw_text)
                #st.write(text_chunks)

            
                #create vector store
                vectorstore=get_vectorstore(text_chunks)
                
                #create conversation chain
                st.session_state.conversation=get_conversation_chain(vectorstore)
                
                
                
if __name__ == "__main__":
    main()
