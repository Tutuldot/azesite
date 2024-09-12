import os 
import psycopg2 
import numpy as np
from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader 
from langchain_community.embeddings import DeepInfraEmbeddings
from langchain.vectorstores.pgvector import PGVector
from langchain_community.chat_models import ChatDeepInfra
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.chains import RetrievalQA

from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter


os.environ["DEEPINFRA_API_TOKEN"] = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK"
CHAT_MODEL = 'meta-llama/Meta-Llama-3-70B-Instruct'

CONNECTION_STRING = "postgresql+psycopg2://postgresadm:3fnosUd8krVC@ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app:5432/resume"
COLLECTION_NAME = 'user_vectors'

embeddings = DeepInfraEmbeddings( model_id="sentence-transformers/clip-ViT-B-32")


vector = PGVector.from_documents(
    embedding=embeddings,
    documents = [],
    collection_name="RESUME_EMBEDDING_AZE",
    connection_string=CONNECTION_STRING,
    use_jsonb=True,
)

system_prompt = (
    "You are a funny and helpful assistant named Chesa You will only answer questions about Anthony Estrada."
    "do not give contact information when not asked"
    "Use the following pieces of retrieved context to answer "
    "the questions. If you don't know the answer, try "
    "to recommend alternatives based on the context."
    "if you really can find the answer recommend to contact him" 
    " Use three sentences maximum and keep the "
    "answer concise."
    ""
    ""
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


'''
query = "freelancer at OTAXI?"
similar = vector.similarity_search_with_score(query, k=5)

for doc in similar:
    print("xxxxxxxxxxxxxxxxxxxxxxx start")
    print(doc[0].page_content, end="\n\n")
    print("xxxxxxxxxxxxxxxxxxxxxxx end\n")



context = "\n".join([doc[0].page_content for doc in similar])
'''
# print(f"related context: {context}")

llm = ChatDeepInfra(model=CHAT_MODEL) 

retriever = vector.as_retriever(search_type="similarity",
    search_kwargs={"k": 3})
print("retriever created...")
'''
qa_stuff = RetrievalQA.from_chain_type(
    llm=chat, 
    chain_type="stuff", 
    retriever=retriever,
    verbose=True,
)


query =  "Anthony Estrada"

response = qa_stuff.run(query)

print(response)
   
'''

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


while True:
    # Prompt the user for input
    user_input = input("Please enter a question (or type 'exit' to quit): ")
    print("\n")
    print(f"User: {user_input}")
    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    response = rag_chain.invoke({"input": user_input})
    rsm = response["answer"]
    print(f"AI Response: {rsm}")

    

