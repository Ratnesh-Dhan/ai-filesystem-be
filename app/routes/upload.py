from flask import Blueprint, request, jsonify
from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex
import os
import threading

upload_bp = Blueprint("upload_bp", __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    print("upload route is called")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    print(file, file.filename, "this is file")
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    upload_dir = './data'
    
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

    try:
        # Ensure the uploads directory exists
        #upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../data"))
        os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
        file.save(os.path.join(upload_dir, file.filename))
        #-----------------------INDEXING STARTING---------------------------------------------------------
        threading.Thread(target=index_document(upload_dir)).start()
        #------------------------INDEXING ENDING-------------------------------------------------------------
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"error": "An error occurred while uploading the file"}), 500  
