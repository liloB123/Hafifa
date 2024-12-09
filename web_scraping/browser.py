from pathlib import Path
import concurrent.futures
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import base64
import asyncio
import aiohttp

chrome_options = Options()
chrome_options.add_argument("--headless")

directory = Path("output")

async def get_html(url, session):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()

async def get_resources(soup):
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
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.save_screenshot(str(dir_path / "screenshot.png"))
    screenshot_path = dir_path / "screenshot.png"

    driver.quit()
    return screenshot_path

def encode_image(screenshot_path):
     with open(screenshot_path, "rb") as image_file:
        screenshot_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        return screenshot_base64
    
async def create_dir(index, url, session, executor):
    dir_name = f"url_{index+1}"

    dir_path = directory / dir_name

    dir_path.mkdir(parents=True, exist_ok=True)

    try:
        screenshot_path = await asyncio.get_event_loop().run_in_executor(executor, get_screenshot, url, dir_path)

        html_response = await get_html(url, session)

        file_name = "browse.json"

        file_path = dir_path / file_name

        soup = BeautifulSoup(html_response, 'html.parser')

        json_data = {
            "html" : html_response,
            "resources" : await get_resources(soup),
            "screenshot" : encode_image(screenshot_path)
        }

        with file_path.open('w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
    
async def main():
    urls_path = Path("input/urls.input")

    if urls_path.exists():
        clean_urls = [url.strip() for url in open(urls_path).readlines()]

        directory.mkdir(parents=True, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            async with aiohttp.ClientSession() as session:
                tasks = [create_dir(index, url, session, executor) for index, url in enumerate(clean_urls)]
                await asyncio.gather(*tasks)

    else:
        print("The path for the urls does not exist")

if __name__ == '__main__':
    asyncio.run(main())

