from langchain.llms import Cohere 
from langchain.chains import LLMChain, RetrievalQA, ConversationChain, ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
#RAG LangChain libs
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS, Chroma, Pinecone

import chainlit as cl
import os
import prompts

llm = Cohere()
os.environ["COHERE_API_KEY"] = ''

DB_FAISS_PATH = 'vectorstore/db_faiss'

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


def Continue_Conversation(message):
    Conv_Agent = ConversationChain(llm=llm,memory=memory)
    resp = Conv_Agent.run({"message": message, "history": memory.memory_key})
    return resp

## RETRIEVE SKILLS AND THEIR WEIGHTS/IMPORTANCE FOR THAT TASK
def TaskReq(task):
    pass

def Recommend(task):
    agent = LLMChain(llm=llm, prompt = AS)
    resp = agent.run({"task": task})
    return resp 

def Explain(task, rank, skills_required, user_skills):
    inputs = {"task": task, "rank": rank, "skills_required": skills_required, "user_skills": user_skills}
    agent = LLMChain(llm=llm, prompt=RE)
    resp = agent.run(inputs)
    return resp

# Create vector database
def create_vector_db(DATA_PATH):
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_FAISS_PATH)

##Local Document RAG system
##### RETRIEVE SKILLS FROM CV -> LEAVE QA AND CONVERSATION TO THE CHAINLIT CODE

#QA the CV
def CV_QA(file):
    # Retrieve vector database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    #Retrieval QA Chain
    qa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       chain_type_kwargs={'prompt': AS},
                                       return_source_documents=True,
                                       )
    response = qa({'file': file})
    return response

#Conversation with CV
def CV_Conv(message):
    # Retrieve vector database
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)

    convret = ConversationalRetrievalChain.from_llm(llm=llm,
                                                  chain_type = "stuff", 
                                                  retriever=db.as_retriever(search_kwargs={'k': 2}),
                                                  memory=memory,
                                                  combine_docs_chain_kwargs={'prompt': AS},
                                                  return_source_documents=True,verbose=False)
    
    response = convret.run({"message": message, "history": memory.memory_key})
    return response

#Chainlit Interface


#chainlit code

@cl.on_chat_start
async def start(prompt):
    welcome_message = """Welcome to the BloomAI PDF QA demo! To get started:
    1. Upload a PDF or text file
    2. Ask a question about the file
    """
    await cl.Avatar(
        name="BloomAI",
        path = "./public/logo_dark.png" ,
    ).send()
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content=welcome_message,
            accept=["text/plain", "application/pdf"],
            max_size_mb=20,
            timeout=180,
            disable_human_feedback=True,
        ).send()

    file = files[0]

    msg = cl.Message(
        content=f"Processing `{file.name}`...", disable_human_feedback=True, author= "BloomAI"
    )
    await msg.send()
 
    # No async implementation in the Pinecone client, fallback to sync
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key = "message",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )
    
    chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type = "stuff", retriever=db.as_retriever(search_kwargs={'k': 2}),memory=memory,combine_docs_chain_kwargs={'prompt': prompt},return_source_documents=True,verbose=True)

    # Let the user know that the system is ready
    msg.content = f"`{file.name}` processed. You can now ask questions! As your tutor, I will try to help answering your questions as much as I can"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_chat_start
async def start(prompt):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    #Retrieval QA Chain
    chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       chain_type_kwargs={'prompt': prompt},
                                       return_source_documents=True,
                                       )
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome!"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain") 
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()