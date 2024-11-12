import marqo
import os
from dotenv import load_dotenv

load_dotenv() 

# Retrieve the Marqo Cloud API key from environment variables for secure access
api_key = os.getenv("MARQO_API_KEY")

# Initialize Marqo client for Marqo Cloud using the API key
mq = marqo.Client("https://api.marqo.ai", api_key=api_key)   # To find your Marqo api key, visit https://www.marqo.ai/blog/finding-my-marqo-api-key

# If you'd rather run Marqo locally, swap out the code above with
# mq = marqo.Client("http://localhost:8882", api_key=None)
# For more information on running Marqo with Docker, see our GitHub: https://github.com/marqo-ai/marqo

# Define the name of the index to retrieve statistics from
index_name = "marqo-ecommerce-search"

# Fetch statistics for the specified index
results = mq.index(index_name).get_stats()

# Print the results to view the statistics of the index
print(results)
