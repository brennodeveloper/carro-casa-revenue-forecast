import os
import joblib
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "final_revenue_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "final_revenue_features.pkl")


def load_model_and_features():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Modelo não encontrado em: {MODEL_PATH}"
        )

    if not os.path.exists(FEATURES_PATH):
        raise FileNotFoundError(
            f"Arquivo de features não encontrado em: {FEATURES_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)

    return model, features


def create_future_scenarios(revenue_model_data, forecast_months=6):
    recent_data = revenue_model_data.tail(6)

    recent_means = recent_data[[
        "monthly_sales",
        "monthly_renewals",
        "monthly_cancellations",
        "monthly_new_customers",
        "average_policy_ticket",
        "estimated_retention_rate"
    ]].mean()

    last_month = revenue_model_data["month"].max()
    last_month_number = revenue_model_data["month_number"].max()

    future_expected = pd.DataFrame({
        "month": pd.date_range(
            start=last_month + pd.DateOffset(months=1),
            periods=forecast_months,
            freq="MS"
        ),
        "month_number": range(
            last_month_number + 1,
            last_month_number + forecast_months + 1
        ),
        "monthly_sales": recent_means["monthly_sales"],
        "monthly_renewals": recent_means["monthly_renewals"],
        "monthly_cancellations": recent_means["monthly_cancellations"],
        "monthly_new_customers": recent_means["monthly_new_customers"],
        "average_policy_ticket": recent_means["average_policy_ticket"],
        "estimated_retention_rate": recent_means["estimated_retention_rate"]
    })

    future_expected["scenario"] = "Expected"

    future_conservative = future_expected.copy()
    future_conservative["monthly_sales"] *= 0.90
    future_conservative["monthly_renewals"] *= 0.90
    future_conservative["monthly_new_customers"] *= 0.90
    future_conservative["average_policy_ticket"] *= 0.95
    future_conservative["estimated_retention_rate"] *= 0.97
    future_conservative["monthly_cancellations"] *= 1.10
    future_conservative["scenario"] = "Conservative"

    future_optimistic = future_expected.copy()
    future_optimistic["monthly_sales"] *= 1.10
    future_optimistic["monthly_renewals"] *= 1.10
    future_optimistic["monthly_new_customers"] *= 1.10
    future_optimistic["average_policy_ticket"] *= 1.05
    future_optimistic["estimated_retention_rate"] *= 1.03
    future_optimistic["monthly_cancellations"] *= 0.90
    future_optimistic["scenario"] = "Optimistic"

    future_scenarios = pd.concat([
        future_conservative,
        future_expected,
        future_optimistic
    ])

    return future_scenarios


def generate_forecast(revenue_model_data):
    model, features = load_model_and_features()

    future_scenarios = create_future_scenarios(revenue_model_data)

    future_scenarios["predicted_revenue"] = model.predict(
        future_scenarios[features]
    )

    forecast_result = future_scenarios[[
        "month",
        "scenario",
        "predicted_revenue"
    ]].copy()

    forecast_result["month"] = forecast_result["month"].astype(str)
    forecast_result["predicted_revenue"] = forecast_result["predicted_revenue"].round(2)

    return forecast_result.to_dict(orient="records")