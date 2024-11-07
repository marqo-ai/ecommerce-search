import marqo
import requests
import io
from PIL import Image
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv() 

# Initialize Marqo client
api_key = os.getenv("MARQO_API_KEY")   # To find your Marqo api key, visit https://www.marqo.ai/blog/finding-my-marqo-api-key
mq = marqo.Client("https://api.marqo.ai", api_key=api_key)

# If you'd rather run Marqo locally, swap out the code above with
# mq = marqo.Client("http://localhost:8882", api_key=None)
# For more information on running Marqo with Docker, see our GitHub: https://github.com/marqo-ai/marqo

def search_marqo(query, themes, negatives):
    """
    Searches Marqo index with a query, additional themes to emphasize, and negative themes to avoid.
    Args:
        query (str): Main search query.
        themes (str): Additional positive theme for emphasis.
        negatives (str): Negative theme to de-emphasize in search.
    Returns:
        list: A list of tuples containing images and associated product information (title, description, price, score).
    """
    # Build query weights
    query_weights = {query: 1.0}
    if themes:
        query_weights[themes] = 0.75
    if negatives:
        query_weights[negatives] = -1.1
    
    # Perform search with Marqo
    res = mq.index("marqo-ecommerce-b").search(query_weights, limit=10)  # limit to top 10 results

    # Prepare results
    products = []
    for hit in res['hits']:
        image_url = hit.get('image_url')
        title = hit.get('title', 'No Title')
        description = hit.get('description', 'No Description')
        price = hit.get('price', 'N/A')
        score = hit['_score']
        
        # Fetch the image from the URL
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))

        # Append product details for Gradio display
        product_info = f'{title}\n{description}\nPrice: {price}\nScore: {score:.4f}'
        products.append((image, product_info))

    return products

def clear_inputs():
    """
    Clears input fields and results in the Gradio interface.
    Returns:
        tuple: Empty values to reset query, themes, negatives, and results gallery.
    """
    return "", "", [], []  # Clears query, themes, negatives, and results

# Gradio Blocks Interface for Custom Layout
with gr.Blocks(css=".orange-button { background-color: orange; color: black; }") as interface:
    gr.Markdown("<h1 style='text-align: center;'>Multimodal Ecommerce Search with Marqo's SOTA Embedding Models</h1>")
    gr.Markdown("### This ecommerce search demo uses:")
    gr.Markdown("### 1. [Marqo Cloud](https://www.marqo.ai/cloud) for the Search Engine.")
    gr.Markdown("### 2. [Marqo-Ecommerce-Embeddings](https://huggingface.co/collections/Marqo/marqo-ecommerce-embeddings-66f611b9bb9d035a8d164fbb) for the multimodal embedding model.")
    gr.Markdown("### 3. 100k products from the [Marqo-GS-10M](https://huggingface.co/datasets/Marqo/marqo-GS-10M) dataset.")

    gr.Markdown("")
    # gr.Markdown("If you can't find the item you're looking for, let a member of our team know and we'll add it to the dataset.")

    with gr.Row():
        query_input = gr.Textbox(placeholder="Green dress shirt", label="Search Query")
        themes_input = gr.Textbox(placeholder="Short sleeves", label="More of...")
        negatives_input = gr.Textbox(placeholder="Patterns", label="Less of...")

    with gr.Row():
        search_button = gr.Button("Submit", elem_classes="orange-button")
        # clear_button = gr.Button("Clear")

    results_gallery = gr.Gallery(label="Top 10 Results", columns=4)

    # Set up function call for search on button click or Enter key
    search_button.click(fn=search_marqo, inputs=[query_input, themes_input, negatives_input], outputs=results_gallery)
    
    # Clear button functionality
    # clear_button.click(fn=clear_inputs, inputs=[], outputs=[query_input, themes_input, negatives_input, results_gallery])

    # Enable Enter key submission for all input fields
    query_input.submit(fn=search_marqo, inputs=[query_input, themes_input, negatives_input], outputs=results_gallery)
    themes_input.submit(fn=search_marqo, inputs=[query_input, themes_input, negatives_input], outputs=results_gallery)
    negatives_input.submit(fn=search_marqo, inputs=[query_input, themes_input, negatives_input], outputs=results_gallery)

# Launch the app
interface.launch()