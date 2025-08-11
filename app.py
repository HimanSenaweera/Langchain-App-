import streamlit as st
from dotenv import load_dotenv #load_dotenv() allows us to use environment variables from a .env file
from PyPDF2 import PdfReader #PyPDF2 is a library for reading PDF files as pages
from langchain.text_splitter import CharacterTextSplitter #CharacterTextSplitter is a class that splits text into chunks based on characters
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import htmlTemplates
from langchain.memory import ConversationBufferMemory

import os

load_dotenv()

#this function will return the pdf as a long single text
def get_pdf_text(pdf_docs):
    text=''
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        #what PdfReader does is it reads the pdf file and returns a list of pages
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text
    #read the pdf_docs and ectract it to pages then read through each of the pages 
    #and extract it and append to a single string with all the content
    
    
def get_text_chunks(text):
    text_splitter=CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  # Size of each chunk
        chunk_overlap=200,  
        # start colleceting the next chunk 200 characters before the end of the previous chunk to retrieve the meaning  otherwise if we start from middle of a sentence it would not have any meaning
        length_function=len
    )
    
    chunks=text_splitter.split_text(text)
    #split_text is a method that splits the text into chunks based on the parameters we set abov
    return chunks
    
    
def get_vectorstore(text_chunks):
    # Use a smaller, faster embedding model
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    # Create conversation chain without deprecated memory
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
    st.session_state.chat_history=response['chat_history']
    for i,message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(htmlTemplates.user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        
        else:
            st.write(htmlTemplates.bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
    
    
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
    
    #st.write(htmlTemplates.user_template.replace("{{MSG}}", "Hello Robot?"), unsafe_allow_html=True)
    #st.write(htmlTemplates.bot_template.replace("{{MSG}}", "Hello! How can I assist you today?"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Upload PDFs")
        pdf_docs=st.file_uploader(
            "Upload PDF files and click on process",accept_multiple_files=True)
        if st.button("Process PDFs"):
            with st.spinner("Processing PDFs..."):
                #get pdf text
                raw_text=get_pdf_text(pdf_docs)
                
                #get the text chunks
                text_chunks=get_text_chunks(raw_text)
                st.write(text_chunks)

            
                #create vector store
                vectorstore=get_vectorstore(text_chunks)
                
                #create conversation chain
                st.session_state.conversation=get_conversation_chain(vectorstore)
                #it takes the history of the conversation and the question and returns the answer
                #this makes it global and not lost when we refresh the page
                
                
if __name__ == "__main__":
    main()