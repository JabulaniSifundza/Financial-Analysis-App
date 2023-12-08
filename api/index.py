from flask import Flask, render_template
import pandas as pd
import yfinance as yf
import requests
import json
import google.generativeai as palm

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("views/index.html")
