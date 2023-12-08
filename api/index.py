from flask import Flask, render_template
import pandas as pd
import yfinance as yf
import requests
import json
from vectordb import Memory

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
