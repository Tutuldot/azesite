import os 
import psycopg2 
import numpy as np
from langchain.text_splitter import CharacterTextSplitter 
from langchain_community.document_loaders import TextLoader 
from langchain_community.embeddings import DeepInfraEmbeddings
from langchain.vectorstores.pgvector import PGVector

from langchain_core.documents import Document


os.environ["DEEPINFRA_API_TOKEN"] = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK"

current_dir = os.path.dirname(os.path.abspath(__file__)) 
file_path = os.path.join(current_dir,"docs","data.txt")

print(f"Current Directory: {current_dir}") 
print(f"Current File path: {file_path}")

loader = TextLoader(file_path) 
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=10) 
texts = text_splitter.split_documents(documents)

print("\n --- Document Chunks Information ---") 
print(f"\n Number of chucks docs: {len(texts)}") 
#print(f"\n Sample chunk: \n {texts[0].page_content}") 
print("\n --- End of Chunks Information ---")


final_docs = []
i = 1
for text in texts:

    if i <= 1:
        final_docs.append(Document(
            page_content=text.page_content
        ))
    i = i + 1



    

print(f"Final Docs Length: {len(final_docs)}")
#embedding
embeddings = DeepInfraEmbeddings( model_id="sentence-transformers/clip-ViT-B-32", deepinfra_api_token = "HTj80cPBu4Qaiw80oIUZAs6J9Nzg73XK")

db_config = { "dbname": "resume", "user": "postgresadm", "password": "3fnosUd8krVC", "host": "ep-autumn-recipe-a1i2wgsj.ap-southeast-1.pg.koyeb.app", "port": 5432 }

#document_result = embeddings.embed_documents(docs[0].page_content)


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
def embedding_function(doc):
    return embeddings.embed_documents([doc])[0]
'''
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


vector = PGVector(
    embedding=embeddings,
    collection_name="RESUME_EMBEDDING_AZE",
    connection_string=CONNECTION_STRING,
    use_jsonb=True,
)


i = 1

for text in texts:
   
    if i > 1:
        print(f"\n Embedding item no: {i} \n {text.page_content[:10]}")
        xxx = []
        xxx.append(Document(
                page_content=text.page_content
            ))


        vector.add_documents(final_docs)
    else:
        print(f"Skipped: {i}")
    i = i + 1







print('embedding completed')
