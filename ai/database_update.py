from langchain.document_loaders import UnstructuredURLLoader
from langchain.indexes import VectorstoreIndexCreator  # Vectorize db index with chromadb
from langchain.embeddings import GooglePalmEmbeddings
from langchain.text_splitter import CharacterTextSplitter  # Text splitter

def update_vector_database(url):
    try:
        loader = UnstructuredURLLoader(urls=[url])
        api_key = google_api_key  # Replace with your actual API key

        index = VectorstoreIndexCreator(
            embedding=GooglePalmEmbeddings(google_api_key=api_key),
            text_splitter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        ).from_loaders([loader])

        return index
    except Exception as e:
        raise Exception(f"Error in creating vector index: {e}")
