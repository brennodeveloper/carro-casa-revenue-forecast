from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
import os
from services.file_service import process_file

upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Processar arquivo
        result = process_file(filepath)

        return jsonify({
            "message": "Arquivo recebido com sucesso",
            "data_preview": result
        }), 200

    return jsonify({"error": "Formato não permitido"}), 400