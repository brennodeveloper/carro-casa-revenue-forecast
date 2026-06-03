from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import Config
import os

from services.data_service import (
    load_monthly_commercial_data,
    validate_monthly_data,
    prepare_revenue_model_data
)

from services.forecast_service import generate_forecast


forecast_bp = Blueprint("forecast", __name__)


def allowed_file(filename):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    )


@forecast_bp.route("/forecast", methods=["POST"])
def forecast_revenue():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Nome de arquivo vazio"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Formato não permitido. Envie CSV ou XLSX."
        }), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        monthly_data, error = load_monthly_commercial_data(filepath)

        if error:
            return jsonify({"error": error}), 400

        is_valid, missing_columns = validate_monthly_data(monthly_data)

        if not is_valid:
            return jsonify({
                "error": "A planilha não possui todas as colunas obrigatórias.",
                "missing_columns": missing_columns
            }), 400

        revenue_model_data = prepare_revenue_model_data(monthly_data)

        forecast = generate_forecast(revenue_model_data)

        return jsonify({
            "message": "Previsão gerada com sucesso",
            "forecast": forecast
        }), 200

    except Exception as error:
        return jsonify({
            "error": "Erro ao gerar previsão.",
            "details": str(error)
        }), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)