from flask import Blueprint
from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex

indexFiles_bp = Blueprint("indexFiles_bp", __name__)

@indexFiles_bp.route("/index-files",  methods=["POST"])
def indexService():
    print("index route is called")
# Reading
    try:
        loader = SimpleDirectoryReader(
            input_dir="./data",
            recursive=True,
        )

        # Loading
        documents = loader.load_data()

        # Indexing
        index = VectorStoreIndex.from_documents(documents)

        index.storage_context.persist(persist_dir='./index_folder') 
    except Exception as e:
        print(e)
        return {"error",  "Error indexing the data"}, 500
    else: 
        print("indexed successfully")
        return {"response": "Data indexed successfully"}, 200