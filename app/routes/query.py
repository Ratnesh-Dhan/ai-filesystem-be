from flask import Blueprint, request, jsonify
from llama_index.core import  StorageContext, load_index_from_storage, get_response_synthesizer
from app.utils.indexLoader import getIndex
import os
import traceback
from app.utils.custom_query import  RAGQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever




query_bp = Blueprint("query_bp", __name__)

@query_bp.route('/query', methods=['POST'])
def query_service():
    print("query route is called")
    
    #------------------------------------------------
        
    # Load the index from the file or database
    
        # retriever = index.as_retriever()
        #query_engine = index.as_query_engine(response_mode="tree_summarize",verbose=True,)


        # retriever=VectorIndexRetriever(
        #     index=index,
        #     similarity_top_k=5,
        # )
        # response_synthesizer = get_response_synthesizer(
        #     response_mode="refine",
        # )
        # query_engine = RAGQueryEngine(retriever=retriever, response_synthesizer=response_synthesizer)
    #-------------------------------------------------------------

    
    
    index = getIndex()
    try:
        if index is None:
           response_data = {
                "answer": "No relevant data found in the provided documents.",
                "sources": [None]
            }
        else:
            if(index) :
                # prompt_template=Prompt(template="only use the most relevant source nodes to answer the question. If you don't find relevant information, say 'No relevant information found.'")
                query_engine = index.as_query_engine(
                    response_mode="compact", 
                    similarity_cutoff=0.7,
                    retrieval_mode="strict"
                )
            data = request.json
            query_text = data.get('query')
            result = query_engine.query(query_text)

            # Get the documents used for the answer
            source_nodes = result.source_nodes
            for node in source_nodes: 
                print(node.score, "Source nodes")
            print(result)



            if source_nodes :
                source_documents = [node.node.metadata.get('file_name', 'Unknown Document') for node in source_nodes]
                #if node.score >= 0.75
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
