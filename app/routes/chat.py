
from flask import Blueprint, request, jsonify
import traceback
from app.utils.indexLoader import getIndex

chat_bp = Blueprint("chat_bp", __name__)
end_chat_bp = Blueprint("end_chat_bp", __name__)

# Dictionary to temporarily store chat context for each session
temporary_sessions = {}

@chat_bp.route('/chat', methods=['POST'])
def chat_service():
    print("chat route is called")
    
    # Get or create a temporary session ID from request headers
    temp_session_id = request.headers.get("Temp-Session-ID")
    
    if not temp_session_id:
        return jsonify({"error": "Temp-Session-ID header is required"}), 400

    try:
        # Check if a session already exists for follow-up
        if temp_session_id in temporary_sessions:
            chat_engine = temporary_sessions[temp_session_id]
        else:
            # Initialize new session with message history
            index = getIndex()
            chat_engine = index.as_chat_engine(
                chat_mode="condense_question",  # Better for follow-up questions
                verbose=True,
                # system_prompt=(
                #     "You are a helpful AI assistant. Use the context provided "
                #     "to answer questions. For follow-up questions, consider the "
                #     "conversation history when providing answers."
                # )
            )
            temporary_sessions[temp_session_id] = chat_engine

        data = request.json
        chat_text = data.get('chat')
        
        # Process the chat input with chat engine
        response = chat_engine.stream_chat(chat_text)
        response_data = "".join(token for token in response.response_gen)
        print(response_data)

        return jsonify({
            "response": response_data,
            "session_id": temp_session_id
        }), 200

    except Exception as e:
        print("chat error", e)
        print(traceback.format_exc())
        return jsonify({"error": "something went wrong with llamaindex"}), 500

# Add a new route to explicitly end sessions
@end_chat_bp.route('/end-chat', methods=['POST'])
def end_chat_session():
    print('end chat route called')
    temp_session_id = request.headers.get("Temp-Session-ID")
    
    if temp_session_id and temp_session_id in temporary_sessions:
        del temporary_sessions[temp_session_id]
        return jsonify({"message": "Chat session ended successfully"}), 200
    
    return jsonify({"error": "Session not found"}), 404