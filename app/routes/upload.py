from flask import Blueprint, request, jsonify
from llama_index.core import  SimpleDirectoryReader, VectorStoreIndex
import os

upload_bp = Blueprint("upload_bp", __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    print("upload route is called")
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check file type
    # if not (file.filename.endswith('.pdf') or file.filename.endswith('.xlsx')):
        
    #     return jsonify({"error": "File type not allowed. Only PDF and Excel files are accepted."}), 400
    
    try:
        # Ensure the uploads directory exists
        #upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../data"))
        upload_dir = './data'
        os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
        file.save(os.path.join(upload_dir, file.filename))
        #-----------------------INDEXING STARTING---------------------------------------------------------
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
        #------------------------INDEXING ENDING-------------------------------------------------------------
        return jsonify({"message": "File uploaded successfully"}), 200
    except Exception as e:
        print("Error occurred: ", e)
        return jsonify({"error": "An error occurred while uploading the file"}), 500  
