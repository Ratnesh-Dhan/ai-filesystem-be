from flask import Blueprint, jsonify, Response
import os

list_files_bp = Blueprint('list_files_bp', __name__)

def listfiles():
    data_dir = './data'
    files = [f for  f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    return files

@list_files_bp.route('/list-files', methods=['GET'])
def list_files_route():
    try:
        files = listfiles()
        response = jsonify({'files': files})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.status_code = 200
        return response
    except Exception as e:
        return jsonify({'error': 'Unable to list files (internal  server error)'}), 500
    

# @lsit_files_bp.route()