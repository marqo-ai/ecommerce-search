import marqo
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv() 

# Initialize the Marqo Cloud Client
print("Initializing Marqo Cloud client...")
api_key = os.getenv("MARQO_API_KEY")   # To find your Marqo api key, visit https://www.marqo.ai/blog/finding-my-marqo-api-key
mq = marqo.Client("https://api.marqo.ai", api_key=api_key)

# If you'd rather run Marqo locally, swap out the code above with
# mq = marqo.Client("http://localhost:8882", api_key=None)
# For more information on running Marqo with Docker, see our GitHub: https://github.com/marqo-ai/marqo

# Read the CSV data file
path_to_data = "data/marqo-gs_100k.csv"
df = pd.read_csv(path_to_data)

# Convert the data into the required document format
print("Converting data into the required document format...")
documents = []
for index, row in df.iterrows():
    document = {
        "image_url": row["image"],
        "query": row["query"],
        "title": row["title"],
        "score": row["score"],
    }
    documents.append(document)
    
    # Print progress for every 1000 rows processed
    if (index + 1) % 1000 == 0:
        print(f"Processed {index + 1} rows...")

print("Data conversion completed. Starting document upload...")

# Add the documents to the Marqo index in batches
batch_size = 64
for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size]
    try:
        print(f"Uploading batch {i // batch_size + 1} (rows {i + 1} to {i + len(batch)})...")
        res = mq.index("marqo-ecommerce-b").add_documents(
            batch,
            client_batch_size=batch_size,
            mappings={
                "image_title_multimodal": {
                    "type": "multimodal_combination",
                    "weights": {"title": 0.1, "query": 0.1, "image_url": 0.8},
                }
            },
            tensor_fields=["image_title_multimodal"],
        )
        print(f"Batch {i // batch_size + 1} upload response: {res}")
    except Exception as e:
        print(f"Error uploading batch {i // batch_size + 1}: {e}")

print("All batches processed.")
