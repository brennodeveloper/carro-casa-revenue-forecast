import os

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from routes.upload_routes import upload_bp
from routes.forecast_routes import forecast_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Criar pasta uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Registrar blueprints
    app.register_blueprint(upload_bp, url_prefix="/api")
    app.register_blueprint(forecast_bp, url_prefix="/api")
    return app


app = create_app()
# app.run(debug=False, port=5001) run é para desenvolvimento, em produção use um servidor como gunicorn ou uwsgi

@app.route("/")
def home():
    return jsonify({
        "message": "API da Corretora Carro & Casa online",
        "status": "running"
    })

@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "revenue-forecast-api"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)