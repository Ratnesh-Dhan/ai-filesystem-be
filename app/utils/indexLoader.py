import os
from llama_index.core import  StorageContext, load_index_from_storage
from flask import jsonify

def getIndex():
    if os.path.exists('./index_folder') and os.listdir('./index_folder'):
        try:
            storage_context = StorageContext.from_defaults(persist_dir='./index_folder')
            index = load_index_from_storage(storage_context)
        except Exception as e:
            print(f"Error while indexing: {e}")
            return jsonify({"error": "something went worng while loading index"}), 500
        else:
            return index
    else:
        return None
