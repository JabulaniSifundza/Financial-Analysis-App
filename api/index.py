import os
from flask import Flask, render_template, jsonify
import pandas as pd
import yfinance as yf
import requests
import json
from bs4 import BeautifulSoup
import google.generativeai as palm
import pdfplumber

app = Flask(__name__, static_folder="static", template_folder="views")
FMP_API_KEY = os.environ.get("FMP_API_KEY")
GOOGLE_PALM_API_KEY = os.environ.get("google_palm_api_key")
symbol = "AAPL"
FMP_ENDPOINT = f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?period=annual&apikey={FMP_API_KEY}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/general", methods=["POST"])
def financial_qna():
    """
    Use the LLM and Financial Books to answer questions
    """
    return "ask me something"


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
