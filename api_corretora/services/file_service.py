import pandas as pd

def process_file(filepath):
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            return {"error": "Formato não suportado"}

        # Retorna apenas preview (primeiras linhas)
        return df.head().to_dict(orient='records')

    except Exception as e:
        return {"error": str(e)}