import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
#from langchain.llms import OpenAI
from langchain.llms import AzureOpenAI
from langchain.vectorstores import Chroma

import constants

deployment_name = 'modelgpt35'
model_name = 'gpt-35-turbo'
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = constants.APIBASE
os.environ["OPENAI_DEPLOYMENT_NAME"] = deployment_name
os.environ["OPENAI_MODEL_NAME"] = model_name
os.environ["OPENAI_API_KEY"] = constants.APIKEY

embeddings_chunk_size = int(constants.EMBEDDINGS_CHUNK_SIZE)
temperature = float(constants.TEMPERATURE)

prompt = None
if len(sys.argv) > 1:
    prompt = sys.argv[1]

embeddings = OpenAIEmbeddings(deployment=deployment_name, model=model_name)

vectorstore = Chroma(persist_directory="persist",
                     embedding_function=embeddings)

# Create an AzureChatOpenAI llm
llm = AzureOpenAI(deployment_name=deployment_name,
                  model_name=model_name, temperature=temperature)

# if os.path.exists("persist"):
#     print("Reusing index...\n")
#     index = VectorStoreIndexWrapper(vectorstore=vectorstore)
# else:
loader = DirectoryLoader("data/")
index = VectorstoreIndexCreator(vectorstore_cls=Chroma,
                                embedding=OpenAIEmbeddings(deployment=deployment_name, model=model_name),
                                vectorstore_kwargs={"persist_directory": "persist"}).from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
    llm=llm, retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1})
)

chat_history = []
while True:
    if not prompt:
        prompt = input("Prompt: ")
    if prompt in ['quit', 'q', 'exit']:
        sys.exit()
    result = chain({"question": prompt, "chat_history": chat_history})
    print(result['answer'])

    chat_history.append((prompt, result['answer']))
    prompt = None
