import os
from flask import Flask, render_template, jsonify
import pandas as pd
import yfinance as yf
import requests
import json
from bs4 import BeautifulSoup
import google.generativeai as palm
import pdfplumber
import textwrap
import numpy as np

app = Flask(__name__, static_folder="static", template_folder="views")
GOOGLE_PALM_API_KEY = os.environ.get("google_palm_api_key")
palm.configure(api_key=GOOGLE_PALM_API_KEY)

GLOBAL_MODEL = None
GLOBAL_PDF_DF = None
GLOBAL_GEN_MODEL = None


FMP_API_KEY = os.environ.get("FMP_API_KEY")
symbol = "AAPL"
FMP_ENDPOINT = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={FMP_API_KEY}"

models = [
    m for m in palm.list_models() if "embedText" in m.supported_generation_methods
]
model = models[0].name


def embed_fn(text):
    return palm.generate_embeddings(model=model, text=text)["embedding"]


def extract_full_pdf(file_path):
    texts = []
    with pdfplumber.open(file_path) as pdf:
        total_pages = len(pdf.pages)
        for i in range(total_pages):
            page = pdf.pages[i]
            texts.append(page.extract_text())
    return tuple(texts)


def find_best_passage(query, dataframe):
    """
    Compute the distances between the query and each document in the dataframe
    using the dot product.
    """
    query_embedding = palm.generate_embeddings(model=model, text=query)
    dot_products = np.dot(
        np.stack(dataframe["Embeddings"]), query_embedding["embedding"]
    )
    idx = np.argmax(dot_products)
    return dataframe.iloc[idx]["Text"]


def make_prompt(query, relevant_passage):
    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
    return textwrap.dedent(
        """You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  Be sure to respond in a complete sentence, being as comprehensive as possible, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a professional, friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """
    ).format(query=query, relevant_passage=escaped)


@app.route("/")
def home():
    global GLOBAL_MODEL, GLOBAL_PDF_DF, GLOBAL_GEN_MODEL
    models = [
        m for m in palm.list_models() if "embedText" in m.supported_generation_methods
    ]
    GLOBAL_MODEL = models[0].name
    PDF_FILE_PATHS = [
        "/static/files/Encyclopedic Dictionary of Finance.pdf",
        "/static/files/Investopedia.pdf",
        "/static/files/Plain English guide to financial terms.pdf",
    ]
    NEW_TEXTS = [extract_full_pdf(path) for path in PDF_FILE_PATHS]
    flat_list = [element for tuple in NEW_TEXTS for element in tuple]
    GLOBAL_PDF_DF = pd.DataFrame(flat_list)
    GLOBAL_PDF_DF.columns = ["Text"]
    GLOBAL_PDF_DF = GLOBAL_PDF_DF[GLOBAL_PDF_DF["Text"] != ""]
    GLOBAL_PDF_DF["Embeddings"] = GLOBAL_PDF_DF["Text"].apply(embed_fn)
    text_models = [
        m
        for m in palm.list_models()
        if "generateText" in m.supported_generation_methods
    ]
    GLOBAL_GEN_MODEL = text_models[0]
    return render_template("index.html")


@app.route("/general", methods=["POST"])
def financial_qna():
    """
    Use the LLM and Financial Books to answer questions
    """
    global GLOBAL_PDF_DF, GLOBAL_GEN_MODEL
    query = "What is the Stock Market?"
    passage = find_best_passage(query, GLOBAL_PDF_DF)
    prompt = make_prompt(query, passage)
    temperature = 0.5
    answer = palm.generate_text(
        prompt=prompt,
        model=GLOBAL_GEN_MODEL,
        candidate_count=3,
        temperature=temperature,
        max_output_tokens=1000,
    )
    for i, candidate in enumerate(answer.candidates):
        print(f"Candidate {i}: {candidate['output']}\n")

    return max(answer.candidates, key=lambda candidate: len(candidate["output"]))


@app.route("/research", methods=["POST"])
def financial_research():
    """
    Use the LLM to read 10Ks and answer questions on the 10Ks
    """
    return "ask me something"


@app.route("/analysis", methods=["POST"])
def financial_analysis():
    """
    Use Pandas and FMP API to analyse stock returns, momentum, volatility and financial statements.
    """
    return "ask me something"


@app.route("/portfolio", methods=["POST"])
def financial_portfolio():
    """
    Portfolio Optimization using Pandas
    """
    return "ask me something"
