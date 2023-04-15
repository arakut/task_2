import requests
import argparse
import os
from dotenv import load_dotenv
from functools import partial

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BITLY_TOKEN = os.getenv('BITLY_TOKEN')
HEADERS = {
    'Authorization': f'Bearer {BITLY_TOKEN}',
}

parser = argparse.ArgumentParser(
    description='A python script that helps you to cut your url or get count of clicks on your bitlink.'
)
parser.add_argument('url', help='Put your link')
user_link = parser.parse_args().url


def shorten_link(user_url):
    main_url = 'https://api-ssl.bitly.com/v4/shorten'

    payload = {
        'long_url': f'{user_url}',
    }

    response = requests.post(main_url, headers=HEADERS, json=payload)
    response.raise_for_status()
    bitlink = response.json().get("id")
    return bitlink


def count_clicks(user_url):
    main_url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}/clicks/summary'

    response = requests.get(main_url, headers=HEADERS)
    response.raise_for_status()
    clicks = response.json().get('total_clicks')
    return clicks


def is_bitlink(user_url):
    main_url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}'

    response = requests.get(main_url, headers=HEADERS)
    if response.ok:
        return True
    return False


def main():
    if is_bitlink(user_link):
        return f'All amounts of clicks: {count_clicks(user_link)}'
    else:
        return f'Your new bitlink: {shorten_link(user_link)}'


if __name__ == '__main__':
    try:
        print(main())
    except requests.exceptions.HTTPError:
        print('Something went wrong with your link')

