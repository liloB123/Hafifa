from pathlib import Path
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import base64

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu") 

driver = webdriver.Chrome(options=chrome_options)

def get_html(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.text

def get_resources(soup):
    resources = []
    
    for img in soup.find_all('img'):
         src = img.get('src')
         if src:
              resources.append(src)
    
    for link in soup.find_all('link', href=True):
                href = link.get('href')
                resources.append(href)

    for script in soup.find_all('script', src=True):
        src = script.get('src')
        resources.append(src)

    return resources

def get_screenshot(url, dir_path):
    driver.get(url)
    screenshot_file = Path("screenshot.png")
    screenshot_path = dir_path / screenshot_file

    return screenshot_path

def encode_image(screenshot_path):
     with open(screenshot_path, "rb") as image_file:
        screenshot_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return screenshot_base64
    
def create_dir(index, url):
    dir_name = f"url_{index+1}"

    dir_path = directory / dir_name

    dir_path.mkdir(parents=True, exist_ok=True)

    try:
        screenshot_path = get_screenshot(url, dir_path)
        driver.save_screenshot(str(screenshot_path))

        html_response = get_html(url)

        file_name = "browse.json"

        file_path = dir_path / file_name

        soup = BeautifulSoup(html_response, 'html.parser')

        json_data = {
            "html" : html_response,
            "resources" : get_resources(soup),
            "screenshot" : encode_image(screenshot_path)
        }

        with file_path.open('w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
    

urls_path = Path("input/urls.input")

if urls_path.exists():
    clean_urls = [url.strip() for url in open(urls_path).readlines()]

    directory = Path("output")
    directory.mkdir(parents=True, exist_ok=True)

    for index, url in enumerate(clean_urls):
        create_dir(index, url)

else:
    print("The path for the urls does not exist")
