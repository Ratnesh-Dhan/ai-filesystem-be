from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex
import os

def index_document(upload_dir):
        try:
            if not os.listdir(upload_dir):
                for root, dirs, files in os.walk('./index_folder'):
                    for file in files:
                        os.remove(os.path.join(root, file))
                print("All files in index_folder have been deleted.")
                return
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


