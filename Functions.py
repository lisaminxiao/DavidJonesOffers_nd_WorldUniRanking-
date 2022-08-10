import numpy as np
from bs4 import BeautifulSoup

from Functions_Get_Html import getHtmlFromUrl


def getLinksToNextPages(URL):
    page = getHtmlFromUrl(URL)  # Receiving data from the page
    soup = BeautifulSoup(page, 'lxml')  # Creating Soup object for parsing
    results = soup.find(id="page-content")  # Finding "page-content" from soup
    PageNumbers = results.find_all("div", class_="page-numbers")
    foundPage = PageNumbers[0]
    foundA = foundPage.find_all("a")
    arrPage = np.array([])

    for curEl in foundA:
        foundhref = curEl.get("href", default="")

        if curEl.text == "next":
            continue
        arrPage = np.append(arrPage, foundhref)

    return arrPage


if __name__ == "__main__":

    URL = "https://www.davidjones.com/gifts/gift-by-occasion/house-warming?src=fh&size=90"
    arrOfPages = getLinksToNextPages(URL)

