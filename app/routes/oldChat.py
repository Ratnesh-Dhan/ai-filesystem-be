# from flask import Blueprint, request, jsonify

# import traceback
# from app.utils.indexLoader import getIndex

# chat_pb = Blueprint("chat_pb", __name__)

# @chat_pb.route('/chat', methods=['POST'])
# def chat_service():
#     print("chat route is called")
#     index = getIndex()
#     try:
#         chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)
#         data = request.json
#         chat_text = data.get('chat')
#         streaming_response = chat_engine.stream_chat(chat_text)
        
        
#     except Exception as e:
#         print("chat error", e)
#         print(traceback.format_exc())
#         return jsonify({"error": "something went wrong with llamaindex"}), 500
#     else:
#         return jsonify({"response": "ok"}), 200





    