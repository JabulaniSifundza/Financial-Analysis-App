import os
from flask import Flask, render_template
import pandas as pd
import yfinance as yf
import requests
import json
import google.generativeai as palm

app = Flask(__name__, static_folder="static", template_folder="views")
FMP_API_KEY = os.environ.get("FMP_API_KEY")
GOOGLE_PALM_API_KEY = os.environ.get("google_palm_api_key")


@app.route("/")
def home():
    return render_template("index.html")
