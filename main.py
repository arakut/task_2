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
    if response.status_code == 200:
        return True
    return False


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']

    chek_link = partial(is_bitlink, token=bitly_token)
    counter = partial(count_clicks, token=bitly_token)
    shorter = partial(shorten_link, token=bitly_token)

    input_link = input('Put your link: ')
    if chek_link(input_link):
        print('All amounts of clicks: ', counter(input_link))
    else:
        print('Your new bitlink: ', shorter(input_link))


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.HTTPError:
        print('Something went wrong with your link')
