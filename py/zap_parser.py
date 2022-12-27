
import re
import time
import requests


def read_url(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    timestamp = time.time()
    r = requests.get(url, allow_redirects=True, headers=user_agent)
    return r.text, timestamp


def parse_text(text, token='data-total-price'):
    lines = text.split('\r\n')

    relevant_lines = list()
    for line in lines:
        if line.find(token) >= 0:
            relevant_lines.append(line)

    return relevant_lines


def extract_prices(lines, token='data-total-price="\d+"'):
    prices = list()
    for line in lines:
        price = float(re.findall('\d+', re.findall(token, line)[0])[0])
        prices.append(price)

    return prices


def calculate_statistics(prices):
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices)/len(prices)
    return dict(min=min_price, max=max_price, avg=avg_price)


def extract_data(raw_data):
    relevant_lines = parse_text(raw_data)
    prices = extract_prices(relevant_lines)
    return prices


def get_model_id(url):
    model_id = re.findall('\d+$', url)[-1]
    return model_id


def process_url(url):
    raw_data, timestamp = read_url(url)
    prices = extract_data(raw_data)
    statistics = calculate_statistics(prices)
    model_id = get_model_id(url)
    statistics['model_id'] = model_id
    statistics['timestamp'] = timestamp
    statistics['url'] = url
    return statistics

def process_urls(urls):
    statistics = list()
    for url in urls:
        s = process_url(url)
        statistics.append(s)

    return statistics
