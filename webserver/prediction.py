import os
import numpy as np
import pandas as pd
import requests
import whois
import joblib
from urllib.parse import urlparse

# Load model once at startup rather than on every request
_model_path = os.path.join(os.path.dirname(__file__), 'KtpCapstoneModel.pkl')
model = joblib.load(_model_path)


def run(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    url_length = len(url)
    special_chars = sum(
        c in [';', '/', '?', ':', '@', '=', '&', '"', "'", '<', '>', ',',
              '.', '[', ']', '\\', '^', '`', '{', '|', '}', '~', '%']
        for c in url
    )

    server = None
    content_length = None
    country = None
    state = None
    reg_days = None
    update_days = None
    tcp_conversation_exchange = None
    dist_remote_tcp_port = None
    remote_ips = None
    app_bytes = None
    source_app_packets = None
    remote_app_packets = None
    source_app_bytes = None
    remote_app_bytes = None
    app_packets = None
    dns_query_times = np.nan

    prediction = 0

    try:
        response = requests.get(url, timeout=5)

        server = response.headers.get('Server')
        content_length = response.headers.get('Content-Length')

        domain = whois.whois(urlparse(url).netloc)
        country = domain.get('country', '')
        state = domain.get('state', '')

        reg_date = domain.get('creation_date', '')
        reg_days = reg_date if reg_date else np.nan

        update_date = domain.get('updated_date', '')
        update_days = update_date if update_date else np.nan

        # Reuse the single response — no duplicate requests
        history = response.history
        tcp_conversation_exchange = len(history)
        dist_remote_tcp_port = len(set(r.status_code for r in history))
        remote_ips = len(set(r.url for r in history))

        app_bytes = len(response.content)
        source_app_packets = app_bytes / 1460
        remote_app_packets = app_bytes / 1460
        source_app_bytes = app_bytes
        remote_app_bytes = app_bytes
        app_packets = app_bytes / 1460

        data = {
            'URL': [url],
            'URL_LENGTH': [url_length],
            'NUMBER_SPECIAL_CHARACTERS': [special_chars],
            'CHARSET': ['UTF-8'],
            'SERVER': [server],
            'CONTENT_LENGTH': [content_length],
            'WHOIS_COUNTRY': [country],
            'WHOIS_STATEPRO': [state],
            'WHOIS_REGDATE': [reg_days],
            'WHOIS_UPDATED_DATE': [update_days],
            'TCP_CONVERSATION_EXCHANGE': [tcp_conversation_exchange],
            'DIST_REMOTE_TCP_PORT': [dist_remote_tcp_port],
            'REMOTE_IPS': [remote_ips],
            'APP_BYTES': [app_bytes],
            'SOURCE_APP_PACKETS': [source_app_packets],
            'REMOTE_APP_PACKETS': [remote_app_packets],
            'SOURCE_APP_BYTES': [source_app_bytes],
            'REMOTE_APP_BYTES': [remote_app_bytes],
            'APP_PACKETS': [app_packets],
            'DNS_QUERY_TIMES': [dns_query_times],
        }

        df = pd.DataFrame(data)
        prediction = model.predict(df)

    except requests.exceptions.ConnectionError:
        prediction = [1]

    return bool(prediction[0]) if hasattr(prediction, '__len__') else bool(prediction)
