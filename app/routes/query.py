from flask import Blueprint, request, jsonify, send_file, Response
from llama_index.core import  StorageContext, load_index_from_storage, get_response_synthesizer
from app.utils.indexLoader import getIndex
import os
import traceback
from app.utils.custom_query import  RAGQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
import json



query_bp = Blueprint("query_bp", __name__)

@query_bp.route('/query', methods=['POST'])
def query_service():
    index = getIndex()
    try:
        if index is None:
            return jsonify({
                "response": {
                    "answer": "No relevant data found in the provided documents.",
                    "sources": []
                }
            }), 200

        query_engine = index.as_query_engine(
            streaming=True,
            response_mode="compact",
            similarity_cutoff=0.7,
            retrieval_mode="strict"
        )
        
        data = request.json
        query_text = data.get('query')
        result = query_engine.query(query_text)

        #source_nodes = result.source_nodes

        # if not source_nodes:
        #     return jsonify({
        #         "response": {
        #             "answer": "No relevant data found in the provided documents.",
        #             "sources": []
        #         }
        #     }), 200

        # source_details = []
        # for node in source_nodes:
        #     source_detail = {
        #         'file_name': node.node.metadata.get('file_name', 'Unknown Document'),
        #         'page_number': node.node.metadata.get('page_label', 'Unknown Page'),
        #         'text_content': node.node.get_content().strip().replace("\n", " ")[:1000],
        #     }
        #     source_details.append(source_detail)

        def generate():
            for text in result.response_gen:
                for char in text:
                    yield char
            # Send sources as the final message
            # yield f"data: SOURCES_START{json.dumps(source_details)}SOURCES_END\n\n"

        return generate(), {'content_type':'application/json' }

    except Exception as e:
        print("Error occurred: ", e)
        print(traceback.format_exc())
        return jsonify({"error": "something went wrong with llamaindex"})
    



@query_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # # Specify the data directory
        # data_dir = './data'
        # file_path = os.path.join(data_dir, filename)
        # print(file_path)
        
        # # Check if file exists and is within the data directory
        # if not os.path.exists(file_path) or not os.path.commonpath([file_path, data_dir]) == data_dir:
        #     print("file not found")
        #     return jsonify({"error": "File not found"}), 404

        # Get the absolute path to the data directory
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(current_dir, 'data')
        file_path = os.path.join(data_dir, filename)
        print(f"Looking for file at: {file_path}")  # Debug print
        
        # Check if file exists and is within the data directory
        if not os.path.exists(file_path) or not os.path.commonpath([file_path, data_dir]) == data_dir:
            print(f"File not found at path: {file_path}")  # Debug print
            return jsonify({"error": "File not found"}), 404
        
        # Send the file as an attachment
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        print("Error occurred: ", e)
        print(traceback.format_exc())
        return jsonify({"error": "Error downloading file"}), 500