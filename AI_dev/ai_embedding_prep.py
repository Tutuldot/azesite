import os 
import psycopg2 
import numpy as np
from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader 
from langchain_community.embeddings import DeepInfraEmbeddings
from langchain.vectorstores.pgvector import PGVector

from langchain_core.documents import Document
from openai import OpenAI



os.environ["DEEPINFRA_API_TOKEN"] = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK"

current_dir = os.path.dirname(os.path.abspath(__file__)) 
file_path = os.path.join(current_dir,"docs","data.txt")

print(f"Current Directory: {current_dir}") 
print(f"Current File path: {file_path}")

loader = TextLoader(file_path) 
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40) 
texts = text_splitter.split_documents(documents)

print("\n --- Document Chunks Information ---") 
print(f"\n Number of chucks docs: {len(texts)}") 
#print(f"\n Sample chunk: \n {texts[0].page_content}") 
print("\n --- End of Chunks Information ---")




#embedding
embeddings = DeepInfraEmbeddings( model_id="sentence-transformers/clip-ViT-B-32", deepinfra_api_token = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK")

db_config = { "dbname": "resume", "user": "postgresadm", "password": "3fnosUd8krVC", "host": "ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app", "port": 5432 }



CONNECTION_STRING = "postgresql+psycopg2://postgresadm:3fnosUd8krVC@ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app:5432/resume"
COLLECTION_NAME = 'user_vectors'

'''
docs2 = [
    Document(
        page_content="there are cats in the pond",
        metadata={"id": 1, "location": "pond", "topic": "animals"},
    ),
    Document(
        page_content="ducks are also found in the pond",
        metadata={"id": 2, "location": "pond", "topic": "animals"},
    )
]
'''
'''
def embedding_function(input):
    response = openai.embeddings.create(
    model="BAAI/bge-large-en-v1.5",
    input=input,
    encoding_format="float"
    )
    return response['data'][0]['embedding']

document_result = embedding_function(texts[5].page_content)



vector = PGVector(
    collection_name="RESUME_EMBEDDING_AZE",
    connection_string=CONNECTION_STRING,
    use_jsonb=True,
    embedding_function=embedding_function
)

'''
#new_document_embeddings = embeddings.embed_documents(texts[0].page_content)


#vector.add_documents(texts)
embeddings = DeepInfraEmbeddings( model_id="sentence-transformers/clip-ViT-B-32")


vector = PGVector.from_documents(
    embedding=embeddings,
    documents = [],
    collection_name="RESUME_EMBEDDING_AZE",
    connection_string=CONNECTION_STRING,
    use_jsonb=True,
)



i = 1

for text in texts:

    try: 

        xxx = [Document(page_content=text.page_content,metadata={"id": i})]
        vector.add_documents(xxx,ids=[doc.metadata["id"] for doc in xxx])
        print(f"done item no: {i}")

    except Exception as e:
        print(f"error item no: {i}  {text.page_content[:10]}")
   
   
   
  
    i = i + 1







print('embedding completed')
