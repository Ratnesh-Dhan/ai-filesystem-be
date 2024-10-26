from flask import Blueprint, request, jsonify
from llama_index.core import  StorageContext, load_index_from_storage, Prompt
from llama_index.core.postprocessor import SimilarityPostprocessor
import os
import traceback
#+++++++++++++++++++++++++
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
#+++++++++++++++++++++++++

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

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    # query
    data = request.json

    response = query_engine.query("what is mecon")
    print("this is what i am looking for ",response)
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    data = request.json
    #print(data.get('query'))

    try:
        #print(storage_context, "this is storage")
        if storage_context is None:
           response_data = {
                "answer": "No relevant data found in the provided documents.",
                "sources": [None]
            }
        else:
            query_text = data.get('query')
            result = query_engine.query(query_text)
            hello= query_engine.retrieve(query_text)
            for node in hello:
                print(node.score)

            # Get the documents used for the answer
            source_nodes = result.source_nodes 
            # with open('source_nodes.txt', 'w') as f:
            #     for node in source_nodes:
            #         f.write("%s\n" % node)
            # print("result", result)
            #print(result, "this is it")
            if source_nodes :
                source_documents = [node.node.metadata.get('file_name', 'Unknown Document') for node in source_nodes]
                # for node in source_nodes:
                #     print(node.node.metadata.get('file_name', 'Unknown Document'))
                # score = [node.score for node in source_nodes]
                # print("score", score)
                # print(source_documents, "source documets")
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
        #print(response)
        #return jsonify({"return": "we are good"})
        return jsonify({"response": response_data}), 200
    #print(response)