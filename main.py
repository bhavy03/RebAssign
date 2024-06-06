import requests
from bs4 import BeautifulSoup

def scrape_and_modify_images(urls, alt_text, new_src_list):
    modified_html_contents = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for i, url in enumerate(urls):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            soup = BeautifulSoup(response.content, 'html.parser')

            image = soup.find('img', alt=alt_text)

            if image and i < len(new_src_list):
                image['src'] = new_src_list[i]

            modified_html_contents.append(image)

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch the webpage {url}: {e}")

    return modified_html_contents


urls = [
    'https://www.zomato.com/mumbai/epitome-lower-parel/menu',
    'https://www.zomato.com/mumbai/p-f-changs-lower-parel/menu',
    'https://www.zomato.com/mumbai/global-fusion-worli/menu',
    'https://www.zomato.com/mumbai/koko-1-lower-parel/menu',
    'https://www.zomato.com/mumbai/hitchki-lower-parel/menu'
]

new_src_list = [
    'https://b.zmtcdn.com/data/menus/966/19363966/00593136957fa986e97a7d1818687ecf.jpg',
    'https://b.zmtcdn.com/data/menus/937/20975937/8850fa3fce43c3fe0d8a343f00eb80a0.jpg',
    'https://b.zmtcdn.com/data/menus/219/18789219/0dba84331fdf2bcbcc2c3cd0f21da7dc.jpg',
    'https://b.zmtcdn.com/data/menus/537/18354537/b49986c0445d2a2e4bce5926723012e6.jpg',
    'https://b.zmtcdn.com/data/menus/172/18548172/53219fbddfe07a24d002bbff5f308dfc.jpg'
]

alt_text = 'Food Menu menu'

modified_html_contents = scrape_and_modify_images(urls, alt_text, new_src_list)
print(modified_html_contents)

def download_images(src_list):
    for i, src in enumerate(src_list):
        try:
            response = requests.get(src)
            response.raise_for_status()  

            with open(f'image_{i+1}.jpg', 'wb') as file:
                file.write(response.content)

            print(f"Image {i+1} downloaded successfully.")

        except requests.exceptions.RequestException as e:
            print(f"Failed to download image {i+1}: {e}")

download_images(new_src_list)
