from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.retrievers import BaseRetriever

class RAGQueryEngine(CustomQueryEngine):
    #"""RAG Query Engine that retrieves data only from the index."""

    # def __init__(self, index, response_synthesizer):
    #     self.retriever = index  # Retrieves only from index
    #     self.response_synthesizer = response_synthesizer  # No external data sources

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    
    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj

