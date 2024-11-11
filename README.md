<a href="https://www.marqo.ai/blog/introducing-marqos-ecommerce-embedding-models">
<img src="https://img.shields.io/badge/Model_Release-Blog-blue?logo=font-awesome&logoColor=white&style=flat&logo=pencil-alt" alt="Blog">
</a>
<a href="https://huggingface.co/collections/Marqo/marqo-ecommerce-embeddings-66f611b9bb9d035a8d164fbb">
    <img src="https://img.shields.io/badge/🤗-Hugging_Face-yellow?logo=hugging-face&logoColor=white&style=flat&logo=pencil-alt" alt="Hugging Face">
</a>
<a href="https://www.marqo.ai/blog/how-to-build-an-ecommerce-image-search-application">
<img src="https://img.shields.io/badge/Ecommerce_Search_-Blog-red?logo=font-awesome&logoColor=white&style=flat&logo=pencil-alt" alt="Blog">
</a>
<a href="https://colab.research.google.com/drive/1Syl9Gde6LguyMjlpDANetbpvBNb9ddxw?usp=sharing">
<img src="https://img.shields.io/badge/🤝_-Open_In_Google_Colab-orange?logo=font-awesome&logoColor=white&style=flat&logo=pencil-alt" alt="Blog">
</a>

# Ecommerce Search with Marqo

This repository contains a multimodal ecommerce search application built using Marqo's [Cloud-based search engine](https://www.marqo.ai/cloud?utm_source=github&utm_medium=organic&utm_campaign=marqo-ai&utm_term=2024-11-07-04-36-utc) and Marqo's state-of-the-art [ecommerce embedding models](https://huggingface.co/collections/Marqo/marqo-ecommerce-embeddings-66f611b9bb9d035a8d164fbb).

<p align="center">
  <img src="assets/ecommerce-demo.gif"/>
</p>

## Step 1. Set Up
First, you will need a Marqo Cloud API Key. To obtain this, visit this [article](https://www.marqo.ai/blog/finding-my-marqo-api-key).
Once you have your API Key, place it inside a `.env` file such that:
```env
MARQO_API_KEY = "XXXXXXXX"   # Visit https://www.marqo.ai/blog/finding-my-marqo-api-key 
```

To install all packages needed for this search demo:
```bash
python3 -m venv venv
source venv/bin/activate   # or venv\Scripts\activate for Windows
pip install -r requirements.txt
```

Now you're ready to create your Marqo Index!

## Step 2: Create Your Marqo Index
For this search demo, we will be using Marqo's state-of-the-art ecommerce embedding models, `marqo-ecommerce-embeddings-B` and `marqo-ecommerce-embeddings-L`. The file `marqo/create_index.py` provides code for each of these models. Feel free to change this to suit whichever model you want. By default, this search demo will use `marqo-ecommerce-embeddings-L`. For more information on these models, see our [Hugging Face](https://huggingface.co/collections/Marqo/marqo-ecommerce-embeddings-66f611b9bb9d035a8d164fbb).

To create your index:
```bash
python3 marqo/create_index.py
python3 marqo/add_documents.py
```

If you visit [Marqo Cloud](https://cloud.marqo.ai/indexes/), you will be able to see the status of your index (and when it's ready to add documents to). The second line here adds data from `data/gs-all-cat-sample-200k.csv` which is a 200k sample of products across all categories from the [Google Shopping](https://huggingface.co/datasets/Marqo/google-shopping-general-eval) dataset. To check the status of your index when documents are being added, you can run:
```bash
python3 marqo/get_stats.py
```
This will tell you how many documents and vectors are in your index. These numbers will continue to increase as more data is added to your index. 

## Step 3: Run the Application
While documents are being added to your index, you can run the UI. To run the search demo:
```bash
python3 app.py
```
This will create a UI exactly like the video at the top of this README.md. 

## Step 4 (Optional): Deploy on Hugging Face
We set up this ecommerce search demo with the ability to deploy onto Hugging Face. Simply set up a Gradio Hugging Face Space and copy the contents of the `app.py` file. Note, you will need to define your Marqo API Key as a secret variable in your Hugging Face Space for this to work. 

To see this demo live on Hugging Face, visit our [Ecommerce Search Space](https://huggingface.co/spaces/Marqo/Ecommerce-Search)!

## Step 5: Clean Up
If you follow the steps in this guide, you will create an index with CPU large inference and a basic storage shard. This index will cost $0.38 per hour. When you are done with the index you can delete it with the following code:
```python
import marqo
import os

mq = marqo.Client("https://api.marqo.ai", api_key=os.getenv("MARQO_API_KEY"))
mq.delete_index(os.getenv(index_name)
```

**If you do not delete your index you will continue to be charged for it.**

## Running This Project Locally
If you'd prefer to run this project locally rather than with Marqo Cloud, you can do so using our [open source version of Marqo](https://github.com/marqo-ai). To run Marqo using Docker:
```bash
docker rm -f marqo
docker pull marqoai/marqo:latest
docker run --name marqo -it -p 8882:8882 marqoai/marqo:latest
```
Once Marqo is running, you can deploy in the same way as above but please note, `mq = marqo.Client("https://api.marqo.ai", api_key=api_key)` will need to be replaced with `mq = marqo.Client("http://localhost:8882", api_key=None)` in `app.py`, `marqo/create_index.py`, `marqo/add_documents.py` and `marqo/get_stats.py`. 

## Questions? Contact Us!
If you have any questions about this search demo or about Marqo's capabilities, you can:
* [Join Our Slack Community](https://join.slack.com/t/marqo-community/shared_invite/zt-2ry33y71j-H0WUeQvFaVlKuuZwl38BeA)
* [Book a Demo](https://www.marqo.ai/book-demo?utm_source=github&utm_medium=organic&utm_campaign=marqo-ai&utm_term=2024-11-07-04-36-utc)
