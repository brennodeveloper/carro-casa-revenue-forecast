# API Corretora - Previsão de Faturamento

API desenvolvida em Flask para processar dados comerciais mensais da corretora Carro & Casa e retornar previsões futuras de faturamento por cenário.

A API recebe uma planilha, valida sua estrutura básica, prepara os dados, carrega um modelo de machine learning previamente treinado e retorna as projeções em formato JSON.

---

## Objetivo

Esta API tem como objetivo disponibilizar o modelo de previsão de faturamento mensal por meio de endpoints HTTP, permitindo que outros sistemas, como um dashboard web, consumam as previsões de forma simples.

A API foi criada para:

- receber planilhas comerciais em formato `.xlsx` ou `.csv`;
- validar se a planilha possui a estrutura mínima esperada;
- processar a aba `comercial_mensal`;
- carregar o modelo treinado salvo em `.pkl`;
- gerar cenários futuros de faturamento;
- retornar os resultados em JSON;
- remover automaticamente arquivos enviados após o processamento.

---

## Tecnologias utilizadas

- Python
- Flask
- Flask-CORS
- Pandas
- OpenPyXL
- Scikit-learn
- Joblib
- Gunicorn
- Render

---

## Estrutura da API

```text
api_corretora/
├── app.py
├── config.py
├── render.yaml
├── requirements.txt
├── models/
│   ├── final_revenue_model.pkl
│   └── final_revenue_features.pkl
├── routes/
│   ├── __init__.py
│   ├── forecast_routes.py
│   └── upload_routes.py
├── services/
│   ├── data_service.py
│   ├── file_service.py
│   └── forecast_service.py
└── uploads/
    └── .gitkeep