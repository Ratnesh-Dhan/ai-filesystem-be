from flask import Blueprint, request, jsonify
from llama_index.core import  StorageContext, load_index_from_storage, Prompt
from llama_index.core.postprocessor import SimilarityPostprocessor
import os
import traceback



query_bp = Blueprint("query_bp", __name__)

@query_bp.route('/query', methods=['POST'])
def query_service():
    print("query route is called")
    
    #------------------------------------------------
    if os.path.exists('./index_folder') and os.listdir('./index_folder'):
        storage_context = StorageContext.from_defaults(persist_dir='./index_folder')
    else:
        storage_context = None
    # Load the index from the file or database
    if(storage_context) :
        index = load_index_from_storage(storage_context)
        # prompt_template=Prompt(template="only use the most relevant source nodes to answer the question. If you don't find relevant information, say 'No relevant information found.'")
        query_engine = index.as_query_engine(
            similarity_cutoff=0.7,
            retrieval_mode="strict"
        )
    #------------------------------------------------

    

    data = request.json

    try:
        if storage_context is None:
           response_data = {
                "answer": "No relevant data found in the provided documents.",
                "sources": [None]
            }
        else:
            query_text = data.get('query')
            result = query_engine.query(query_text)

            # Get the documents used for the answer
            source_nodes = result.source_nodes 
            #print(source_nodes[0].score, "Source nodes 0")


            if source_nodes :
                source_documents = [node.node.metadata.get('file_name', 'Unknown Document') for node in source_nodes if node.score >= 0.78]
                response_data = {
                    "answer": str(result.response),
                    "sources": list(set(source_documents))
                }
            else:
                response_data = {
                    "answer": "No relevant data found in the provided documents.",
                    "sources": []
                }

    except  Exception as e:
        print("Error occurred: ", e)
        print(traceback.format_exc())
        return jsonify({"error": "something went worng with llamaindex"})
    
    else:
        return jsonify({"response": response_data}), 200
