import marqo
import os
from dotenv import load_dotenv

load_dotenv() 

# Initialize Marqo Cloud Client
# Fetch API key from environment variable for secure access
api_key = os.getenv("MARQO_API_KEY")   # To find your Marqo api key, visit https://www.marqo.ai/blog/finding-my-marqo-api-key
mq = marqo.Client("https://api.marqo.ai", api_key=api_key)

# If you'd rather run Marqo locally, swap out the code above with
# mq = marqo.Client("http://localhost:8882", api_key=None)
# For more information on running Marqo with Docker, see our GitHub: https://github.com/marqo-ai/marqo

# Define settings for the Marqo index
settings = {
    "type": "unstructured",
    "model": "Marqo/marqo-ecommerce-embeddings-L",  # Specify alternative model
    "modelProperties": {
        "name": "hf-hub:Marqo/marqo-ecommerce-embeddings-L",
        "dimensions": 1024,  # Larger dimensionality for embeddings
        "type": "open_clip"
    },
    "treatUrlsAndPointersAsImages": True,  # Enable image URLs as image sources
    "inferenceType": "marqo.CPU.large",  # Inference type for Marqo Cloud resources
}

# Specify the name of the index
index_name = "marqo-ecommerce-search"

# Delete the existing index if it already exists to avoid conflicts
try:
    mq.index(index_name).delete()
except:
    pass  # If the index does not exist, skip deletion

# Create a new index with the specified settings
mq.create_index(index_name, settings_dict=settings)

# Alternative model configuration: marqo-ecommerce-embeddings-B 
# settings = {
#     "type": "unstructured",  # Set the index type as unstructured data
#     "model": "Marqo/marqo-ecommerce-embeddings-B",  # Specify model name
#     "modelProperties": {  # Set model properties to use Marqo's ecommerce embeddings on HF Hub
#         "name": "hf-hub:Marqo/marqo-ecommerce-embeddings-B",
#         "dimensions": 768,  # Dimensionality of the embedding model
#         "type": "open_clip"  # Model type (OpenCLIP architecture)
#     },
#     "treatUrlsAndPointersAsImages": True,  # Enable image URLs as image sources
#     "inferenceType": "marqo.CPU.large",  # Inference type for Marqo Cloud resources
# }