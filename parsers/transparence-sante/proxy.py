import os

from settings import PROXY_FILE


def load_proxies():
    if os.path.isfile(PROXY_FILE):
        return [p for p in open(PROXY_FILE).read().split('\n') if p != ''] + [None]
    else:
        return [None]

proxies = load_proxies()

print proxies