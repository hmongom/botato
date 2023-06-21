import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from . import browserPath

def getLink(query: str):
    query = query.replace(" ", "+")
    query = f"https://clavecd.es/catalog/search-{query}"

    html = BeautifulSoup(requests.get(query).text, "lxml")
    try:
        link = html.find("li", class_ = "search-results-row").find("a").get("href")
    except AttributeError:
        raise Exception()

    return link

def getTitle(link: str):
    soup = BeautifulSoup(requests.get(link).text, "lxml")

    title = soup.find("div", class_ = "content-box-title").find("span", attrs = {"data-itemprop": "name"}).get_text()
    title = title.replace("\n", "").replace("\t", "")
    return title

def scrapKeys(link: str):
    options = Options()
    options.add_argument("--headless")
    options.binary_location = browserPath
    service = Service(executable_path = "./chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service = service, options = options)

    driver.get(link)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "lxml")

    title = soup.find("div", class_ = "content-box-title").find("span", attrs = {"data-itemprop": "name"}).get_text()
    title = title.replace("\n", "").replace("\t", "")

    table = soup.find("div", id = "offers_table")
    keys = table.find_all("div", class_ = "offers-table-row x-offer")

    content = ""
    for i, key in enumerate(keys):
        if (i == 5 or i == len(keys)):
            break     
        info = "[ " + key.find("div", class_ = "x-offer-edition-region-names offers-infos d-block d-md-none").get_text(separator = " - ") + " ]"
        store = key.find("div", class_ = "x-offer-merchant-title offers-merchant text-truncate").get("title")
        price = key.find("div", class_ = "offers-table-row-cell buy-btn-cell").find("span").get_text()
        content += f"\n{info}    {price} {store}"

    return title, content