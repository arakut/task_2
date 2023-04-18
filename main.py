import requests
import os
from dotenv import load_dotenv
from functools import partial


def shorten_link(user_url, token):
    main_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {token}',
    }

    payload = {
        'long_url': f'{user_url}',
    }

    response = requests.post(main_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json().get("id")
    return bitlink


def count_clicks(user_url, token):
    main_url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}/clicks/summary'

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(main_url, headers=headers)
    response.raise_for_status()
    clicks = response.json().get('total_clicks')
    return clicks


def is_bitlink(user_url, token):
    main_url = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}'

    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(main_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']

    input_link = input('Put your link: ')

    try:
        chek_link = is_bitlink(input_link, bitly_token)

        if chek_link:
            counter = count_clicks(input_link, bitly_token)
            print('All amounts of clicks:', counter)
        else:
            shorter = shorten_link(input_link, bitly_token)
            print('Your new bitlink:', shorter)
    except requests.exceptions.HTTPError:
        print('Something went wrong with your link')


if __name__ == '__main__':
    main()
