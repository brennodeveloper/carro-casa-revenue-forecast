import pandas as pd


REQUIRED_COLUMNS = [
    "mes_referencia",
    "quantidade_vendas_mes",
    "quantidade_renovacoes_mes",
    "quantidade_cancelamentos_mes",
    "quantidade_novos_clientes_mes",
    "ticket_medio_apolice_mes",
    "taxa_retencao_estimada_percentual",
    "faturamento_mensal"
]


def load_monthly_commercial_data(filepath):
    try:
        df = pd.read_excel(filepath, sheet_name="comercial_mensal")
        return df, None
    except Exception as error:
        return None, f"Erro ao ler a aba comercial_mensal: {str(error)}"


def validate_monthly_data(df):
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        return False, missing_columns

    return True, []


def prepare_revenue_model_data(df):
    df = df.copy()

    df["mes_referencia"] = pd.to_datetime(df["mes_referencia"])
    df = df.sort_values("mes_referencia")

    revenue_model_data = df[REQUIRED_COLUMNS].copy()

    revenue_model_data = revenue_model_data.rename(columns={
        "mes_referencia": "month",
        "quantidade_vendas_mes": "monthly_sales",
        "quantidade_renovacoes_mes": "monthly_renewals",
        "quantidade_cancelamentos_mes": "monthly_cancellations",
        "quantidade_novos_clientes_mes": "monthly_new_customers",
        "ticket_medio_apolice_mes": "average_policy_ticket",
        "taxa_retencao_estimada_percentual": "estimated_retention_rate",
        "faturamento_mensal": "monthly_revenue"
    })

    revenue_model_data["month_number"] = range(1, len(revenue_model_data) + 1)

    return revenue_model_data