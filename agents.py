from langchain.llms import Cohere 
from langchain.chains import LLMChain, RetrievalQA, ConversationChain, ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
#RAG LangChain libs
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from typing import List 
import prompts
import requests
import numpy as np 
import faiss

llm = Cohere(cohere_api_key="")

DB_FAISS_PATH = 'vectorstore/db_faiss'


STR = prompts.SingleTaskReq
TR = prompts.TasksReq
SK = prompts.SkillRetrieval
TN = prompts.TaskNovelty
CVQA = prompts.CVQA
SGT = prompts.SuggestTask
AS = prompts.AllocationStrategies
RE = prompts.TaskRankExplanation

message_history = ChatMessageHistory()

memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key = "message",
    output_key="answer",
    chat_memory=message_history,
    return_messages=True,
)

def Conversation(message: str):
    Conv_Agent = ConversationChain(llm=llm,memory=memory)
    resp = Conv_Agent.run({"message": message, "chat_history": memory.buffer})
    memory.chat_memory.add_ai_message(resp)
    memory.chat_memory.add_user_message(message)
    return resp

def TaskReq(task: str):
    agent = LLMChain(llm=llm, prompt = STR)
    resp = agent.run({"task": task})
    memory.chat_memory.add_ai_message(resp)
    memory.chat_memory.add_message(task)
    return resp 

def SuggestTasks(skills: str):
    agent = LLMChain(llm=llm, prompt = SGT)
    resp = agent.run({"skills": skills})
    memory.chat_memory.add_ai_message(resp)
    memory.chat_memory.add_message(skills)
    return resp 

def Recommend(task):
    agent = LLMChain(llm=llm, prompt = AS)
    resp = agent.run({"task": task})
    memory.chat_memory.add_ai_message(resp)
    memory.chat_memory.add_message(task)
    return resp 

def Explain(task, rank, skills_required, user_skills):
    inputs = {"task": task, "rank": rank, "skills_required": skills_required, "user_skills": user_skills}
    agent = LLMChain(llm=llm, prompt=RE)
    resp = agent.run(inputs)
    memory.chat_memory.add_ai_message(resp)
    memory.chat_memory.add_message(task)
    return resp

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": "Bearer hf_"}

def get_embedding(text):
    """
    Get embeddings for a given text using the Hugging Face API.
    """
    payload = {
        "inputs": text
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get embeddings: {response.status_code}, {response.text}")
    
    
# Create vector database
def create_vector_db(DATA_PATH):
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    
    text_chunks = [text.page_content for text in texts]
        
    embeddings = []
    for chunk in text_chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)

    # Convert embeddings to a numpy array
    embeddings_array = np.array(embeddings).astype('float32')

    # Create a FAISS index
    dimension = embeddings_array.shape[1]  # Dimension of the embeddings
    index = faiss.IndexFlatL2(dimension)  # L2 distance index
    index.add(embeddings_array)  # Add embeddings to the index

    # Save the FAISS index to disk
    faiss.write_index(index, DB_FAISS_PATH)
    
        
    # embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/multi-qa-mpnet-base-dot-v1',
    #                                    model_kwargs={'device': 'cpu'})

    # db = FAISS.from_documents(texts, embeddings)
    # db.save_local(DB_FAISS_PATH)


##Local Document RAG system

def Retrieve_SKills():
    # Retrieve vector database
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #                                    model_kwargs={'device': 'cpu'})
    # db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    db = faiss.read_index(DB_FAISS_PATH)
    #Retrieval QA Chain
    qa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       chain_type_kwargs={'prompt':SK},
                                       return_source_documents=True,
                                       )
    response = qa.run("Extract skills from the CV.")
    memory.chat_memory.add_ai_message(response)
    return response

def TaskNovelty(task: str): #task name
    # Retrieve vector database
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #                                    model_kwargs={'device': 'cpu'})
    # db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    db = faiss.read_index(DB_FAISS_PATH)
    #Retrieval QA Chain
    qa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       chain_type_kwargs={'prompt':TN},
                                       return_source_documents=True,
                                       )
    response = qa.run({"task": task})
    memory.chat_memory.add_ai_message(response)
    return response


#Conversation with CV (QA)
def CV_Chat(message: str):
    # Retrieve vector database
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
    #                                    model_kwargs={'device': 'cpu'})
    # db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    db = faiss.read_index(DB_FAISS_PATH)
    convret = ConversationalRetrievalChain.from_llm(llm=llm,
                                                  chain_type = "stuff", 
                                                  retriever=db.as_retriever(search_kwargs={'k': 2}),
                                                  memory=memory,
                                                  combine_docs_chain_kwargs={'prompt': CVQA},
                                                  return_source_documents=True,verbose=False)
    
    response = convret.run({"message": message})
    memory.chat_memory.add_user_message(message)
    return response
