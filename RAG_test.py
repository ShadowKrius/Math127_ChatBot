
# loading the pdf data

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFLoader

def load_documents():
    document_loader = PyPDFDirectoryLoader("documents")
    return document_loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

def split_documents(document: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function = len,
        is_separator_regex = False,
    )
    return text_splitter.split_documents(document)

# generating the embeddings
# next we create an embedding for each chunk
# this will become something like a key for a database


from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
    embeddings = BedrockEmbeddings(
        credentials_profile_name = "default",
        region_name = "us-east-1"
    )
    return embeddings

# creating the database
# once we have the document split into smaller chunks, 
# we can use the embedding function to build a vector database with it.

from langchain.vectorstores.chroma import Chroma

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory = "chroma",
        embedding_function = get_embedding_function()
    )
    db.add_documents(chunks)
    db.persist()

# documents = load_documents()
# chunks = split_documents(documents)
# print(chunks[0])