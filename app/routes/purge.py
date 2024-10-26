import os
import shutil
from flask import Blueprint, jsonify

purge_bp = Blueprint("purge_bp", __name__)

def truncate_directory(target_dir):
    if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        print(f"Everything inside {target_dir} deleted successfully.")
    else:
         print(target_dir+" directory does not exist.")

@purge_bp.route("/purge",  methods=["POST"])
def purge():
    try:
        truncate_directory('./data')
        truncate_directory('./index_folder')
    except Exception as e:
        print(f"Error deleting data directory: {e}")
        return jsonify({"error": "Failed to purge directories"}), 500
    else:
        return jsonify({"response": "Purge successfully"}), 200