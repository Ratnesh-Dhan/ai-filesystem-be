from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex

def index_document(upload_dir):
        try:    
            loader = SimpleDirectoryReader(
                input_dir=upload_dir,
                recursive=False,
                #num_files_limit=1
            )

            # Loading
            documents = loader.load_data()

            # Indexing
            index = VectorStoreIndex.from_documents(documents)

            index.storage_context.persist(persist_dir='./index_folder')
            print("Index succesfull")
        except Exception as e:
            print(f"Error indexing document: {e}")


