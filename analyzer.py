def analyze_item(image_path: str, user_text: str = ""):
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    
    prompt = f"""You are a resale expert. Analyze this item for resale value.
User description: {user_text}
Extract: brand, model, condition (1-10), defects, category, key features."""

    response = ollama.chat(
        model='llava:7b',          # Changed here
        messages=[{'role': 'user', 'content': prompt, 'images': [img_bytes]}]
    )
    return response['message']['content']
