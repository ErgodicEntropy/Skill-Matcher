#local document RAG system

from langchain.chains import LLMChain, ConversationChain
from langchain.llms import Cohere 
import chainlit as cl
from llm import qa_bot
import prompts

llm = Cohere()

AS = prompts.AllocationStrategies
RE = prompts.TaskRankExplanation
CP = prompts.CP

def Recommend(task):
    agent = LLMChain(llm=llm, prompt = AS)
    resp = agent.run({"task": task})
    return resp 

def Explain(task, rank, energy_required, user_energy):
    inputs = {"task": task, "rank": rank, "energy_required": energy_required, "user_energy": user_energy}
    agent = LLMChain(llm=llm, prompt=RE)
    resp = agent.run(inputs)
    return resp

#output function without chainlit
def respond(query, prompt):
    qa_result = qa_bot(prompt)
    response = qa_result({'query': query})
    return response


#chainlit code
@cl.on_chat_start
async def start(prompt):
    chain = qa_bot(prompt)
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to BloomAI. What is your question?"
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
    # sources = res["source_documents"]

    # if sources:
    #     answer += f"\nSources:" + str(sources)
    # else:
    #     answer += "\nNo sources found"

    await cl.Message(content=answer).send()








#User Document RAG system



from langchain.llms import huggingface_hub, HuggingFaceHub
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS, Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
from chainlit.types import AskFileResponse


    


namespaces = set()

welcome_message = """Welcome to the BloomAI PDF QA demo! To get started:
1. Upload a PDF or text file
2. Ask a question about the file
"""

llm = load_llm()


@cl.on_chat_start
async def start():
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
    docsearch = await cl.make_async(get_docsearch)(file)

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key = "context",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )
    
    chain = ConversationalRetrievalChain.from_llm(llm=llm,chain_type = "stuff", retriever=docsearch.as_retriever(search_kwargs={'k': 2}),memory=memory,combine_docs_chain_kwargs={'prompt': prompt2},return_source_documents=True,verbose=True)

    # Let the user know that the system is ready
    msg.content = f"`{file.name}` processed. You can now ask questions! As your tutor, I will try to help answering your questions as much as I can"
    await msg.update()

    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")  # type: ConversationalRetrievalChain
    cb = cl.AsyncLangchainCallbackHandler()
    res = await chain.acall(message.content, callbacks=[cb])
    answer = res["answer"]
    # source_documents = res["source_documents"]  # type: List[Document]

    # text_elements = []  # type: List[cl.Text]

    # if source_documents:
    #     for source_idx, source_doc in enumerate(source_documents):
    #         source_name = f"source_{source_idx}"
    #         # Create the text element referenced in the message
    #         text_elements.append(
    #             cl.Text(content=source_doc.page_content, name=source_name)
    #         )
    #     source_names = [text_el.name for text_el in text_elements]

    #     if source_names:
    #         answer += f"\nSources: {', '.join(source_names)}"
    #     else:
    #         answer += "\nNo sources found"

    await cl.Message(content=answer, author ="BloomAI", disable_human_feedback=False).send()
    

    
    