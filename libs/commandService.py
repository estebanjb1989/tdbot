#!/usr/bin/env python3
# BINANCE
import urllib.parse
import urllib.request
from urllib.parse import urljoin, urlencode
import json
import hashlib
import hmac
import time
from datetime import datetime
import requests

BASE_URL = 'https://api.binance.com'
apiKey = ''
secret = ''

def set_config(api_key, api_secret):
    apiKey = api_key
    secret = api_secret


def create_sell_order_limit(quantity, limitPrice):
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    headers = {
        'X-MBX-APIKEY': apiKey
    }
    params = {
        'recvWindow': 5000,
        'timestamp': timestamp,
        'side': "SELL",
        'symbol': 'BTCUSDT',
        'quantity': quantity,
        'type': "LIMIT",
        'timeInForce': "GTC",
        'price': limitPrice,
        'timestamp': time.time(),
        'recvWindow': 6000
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret.encode(
        'utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)
    dataSet = r.json()
    return dataSet

def create_buy_order_market(quantity):
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    headers = {
        'X-MBX-APIKEY': apiKey
    }
    params = {
        'recvWindow': 5000,
        'timestamp': timestamp,
        'side': "BUY",
        'symbol': 'BTCUSDT',
        'quantity': quantity,
        'type': "MARKET",
        'timeInForce': "GTC",
        'timestamp': time.time(),
        'recvWindow': 6000
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret.encode(
        'utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)
    dataSet = r.json()
    return dataSet

def create_buy_order_limit(quantity, limitPrice):
    PATH = '/api/v3/order'
    timestamp = int(time.time() * 1000)
    headers = {
        'X-MBX-APIKEY': apiKey
    }
    params = {
        'recvWindow': 5000,
        'timestamp': timestamp,
        'side': "BUY",
        'symbol': 'BTCUSDT',
        'quantity': quantity,
        'type': "LIMIT",
        'timeInForce': "GTC",
        'price': limitPrice,
        'timestamp': time.time(),
        'recvWindow': 6000
    }
    query_string = urllib.parse.urlencode(params)
    params['signature'] = hmac.new(secret.encode(
        'utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    url = urljoin(BASE_URL, PATH)
    r = requests.post(url, headers=headers, params=params)
    dataSet = r.json()
    return dataSet


# def get_balances():
#     PATH = '/api/v3/account'
#     timestamp = int(time.time() * 1000)
#     headers = {
#         'X-MBX-APIKEY': apiKey
#     }
#     params = {
#         'recvWindow': 5000,
#         'timestamp': timestamp
#     }
#     query_string = urllib.parse.urlencode(params)
#     params['signature'] = hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
#     url = urljoin(BASE_URL, PATH)
#     r = requests.get(url, headers=headers, params=params)
#     dataSet = r.json()
#     return dataSet
