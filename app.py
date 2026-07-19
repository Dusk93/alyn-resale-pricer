import gradio as gr
from analyzer import analyze_item
from pricer import get_comparables, generate_price_estimate

def render_pricing(image, text_desc):
    if not image:
        return "Upload image", "No data", "<h2>Upload a photo</h2>", None
    
    analysis = analyze_item(image, text_desc)
    df_comps = get_comparables(analysis)
    estimate = generate_price_estimate(analysis, df_comps)
    
    price_html = f"""
    <div style="background: linear-gradient(135deg, #22c55e, #15803d); color:white; padding:25px; border-radius:15px; text-align:center;">
        <h1 style="margin:0;">${estimate['median']}</h1>
        <p style="margin:5px 0;">Suggested Resale Price</p>
        <p><strong>${estimate['low']} — ${estimate['high']}</strong></p>
        <p>Confidence: {estimate['confidence']}</p>
    </div>
    """
    
    return analysis, estimate['reasoning'], price_html, df_comps

with gr.Blocks(title="AI Resale Pricer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛍️ AI Resale Pricer\n**Local • Free • Private**")
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="filepath", label="📸 Item Photo", height=380)
            text_input = gr.Textbox(lines=4, placeholder="Extra details (condition, brand, etc.)", label="Description")
            btn = gr.Button("Analyze & Price", variant="primary", size="large")
        
        with gr.Column():
            analysis_out = gr.Textbox(label="🔍 Analysis", lines=10)
            reasoning_out = gr.Textbox(label="💰 Pricing Reasoning", lines=8)
    
    gr.Markdown("### 💵 Recommended Price")
    price_display = gr.HTML()
    
    gr.Markdown("### 📊 Comparables")
    table = gr.Dataframe(label="Recent Sold Items")
    
    btn.click(render_pricing, [image_input, text_input], [analysis_out, reasoning_out, price_display, table])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)