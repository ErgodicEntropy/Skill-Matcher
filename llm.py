#Local Document RAG system


from langchain.llms import huggingface_hub, HuggingFaceHub, Cohere
from langchain.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS, Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
from chainlit.types import AskFileResponse
import prompts


llm = Cohere()

DATA_PATH = './data/The-Encyclopedia-of-Philosophy-2nd-Ed.-Vol.-1.pdf' #or any Domain pdf

#QA Model Function
def qa_bot(prompt):
    # Create vector database
    loader = DirectoryLoader(DATA_PATH,glob='*.pdf',loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',model_kwargs={'device': 'cpu'})
    db = FAISS.from_documents(texts, embeddings)
    #load llm
    llm = llm
    #Retrieval QA Chain
    qa = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )

    return qa
















#User Document RAG system



index_name = "langchain-demo"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

namespaces = set()

welcome_message = """Welcome to the BloomAI PDF QA demo! To get started:
1. Upload a PDF or text file
2. Ask a question about the file
"""


def process_file(file: AskFileResponse):
    import tempfile

    if file.type == "text/plain":
        Loader = TextLoader
    elif file.type == "application/pdf":
        Loader = PyPDFLoader

    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tempfile:
        if file.type == "text/plain":
            tempfile.write(file.content)
        elif file.type == "application/pdf":
            with open(tempfile.name, "wb") as f:
                f.write(file.content)

        loader = Loader(tempfile.name)
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        for i, doc in enumerate(docs):
            doc.metadata["source"] = f"source_{i}"
        return docs


def get_docsearch(file: AskFileResponse):
    docs = process_file(file)

    # Save data in the user session
    cl.user_session.set("docs", docs)

    # Create a unique namespace for the file
    namespace = str(hash(file.content))
    docsearch = Chroma.from_documents(
        docs, embeddings
        )
    return docsearch

    # if namespace in namespaces:
    #     docsearch = Pinecone.from_existing_index(
    #         index_name=index_name, embedding=embeddings, namespace=namespace
    #     )
    # else:
    #     docsearch = Pinecone.from_documents(
    #         docs, embeddings, index_name=index_name, namespace=namespace
    #     )
    #     namespaces.add(namespace)

    # return docsearch


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
    

    
    