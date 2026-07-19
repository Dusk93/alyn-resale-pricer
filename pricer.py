import pandas as pd

def get_comparables(analysis: str):
    try:
        return pd.read_csv("comparables.csv").head(8)
    except:
        return pd.DataFrame([{"title": "Similar Item", "price": 45}])

def generate_price_estimate(analysis: str, comps_df: pd.DataFrame):
    prompt = f"Item Analysis: {analysis}\n\nComparables:\n{comps_df.to_string()}\nGive realistic price range and tips."
    response = ollama.generate(model='llama3.2', prompt=prompt)
    text = response['response']
    return {
        "reasoning": text,
        "low": 40,
        "median": 65,
        "high": 90,
        "confidence": "Medium"
    }
