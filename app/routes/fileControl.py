from flask import Blueprint, jsonify, request
from app.utils.indexDocument import  index_document
import threading
import os

list_files_bp = Blueprint('list_files_bp', __name__)
delete_files_bp = Blueprint('delete_files_bp', __name__)

def listfiles():
    data_dir = './data'
    files = [f for  f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    return files

@list_files_bp.route('/list-files', methods=['GET'])
def list_files_route():
    try:
        files = listfiles()
        response = jsonify({'files': files})
        #response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': 'Unable to list files (internal  server error)'}), 500

@delete_files_bp.route('/delete-files', methods=['DELETE'])
def delete_files_route():
    try:
        data_dir = './data'
        # Get file names from request JSON
        files_to_delete = request.get_json().get('files', [])
        
        deleted_files = []
        not_found_files = []
        
        for filename in files_to_delete:
            file_path = os.path.join(data_dir, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                deleted_files.append(filename)
            else:
                not_found_files.append(filename)

        #-----------------------INDEXING STARTING---------------------------------------------------------
        threading.Thread(target=index_document, args=(data_dir,)).start()
        #------------------------INDEXING ENDING----------------------------------------------------------
        
        return jsonify({
            'message': 'Files processed',
            'deleted': deleted_files,
            'not_found': not_found_files
        }), 200
    except Exception as e:
        return jsonify({'error': 'Unable to delete files (internal server error)'}), 500