import numpy as np
from bs4 import BeautifulSoup
from Functions_Get_Html import getHtmlFromUrl
import pandas as pd

from Functions import getLinksToNextPages


def getPrice_ItemName_Discount_fromWebsite(
        URL):  # Getting the information(item name, price and discount) from the website
    page = getHtmlFromUrl(URL)  # Receiving data from the page
    soup = BeautifulSoup(page, 'lxml')  # Creating Soup object for parsing
    results = soup.find(id="page-content")  # Finding "page-content" from soup
    print(URL)
    try:  # try to run detail_products_whole
        detail_products_whole = results.find("div", class_="products")  # Finding all "products" from the "page-content"
    except:  # if try won't work, run again
        page = getHtmlFromUrl(URL)  # Receiving data from the page
        soup = BeautifulSoup(page, 'lxml')  # Creating Soup object for parsing
        results = soup.find(id="page-content")  # Finding "page-content" from soup
        detail_products_whole = results.find("div", class_="products")

    eachOne = detail_products_whole.find_all("div", class_="item")  # Finding all "item" from the whole products

    df = pd.DataFrame([], columns=["name", "prices", "offers"])  # Creating dataframe

    for curItem in eachOne:  # Looping curItem in eachOne
        cur_linkAndName = curItem.find("h4")  # Finding "h4" in curItem which is in eachOne and name it cur_lingAndName
        if cur_linkAndName == None:  # if cur_linkAndName is empty
            continue  # continue if cur_linkAndName is empty
        cur_linkAndName = cur_linkAndName.find("a")  # Finding "a" in cur_linkAndName and name it cur_linkAndName
        cur_linkAndName = cur_linkAndName.text  # Collect text information in cur_linkAndName and name it cur_linkAndName

        price = float(
            curItem.find("p", class_="price").find("span", class_="price-display").text.replace("$", "").replace(",",
                                                                                                                 ""))

        try:
            offers = curItem.find("p", class_="offer")  # Finding class_=offer under "p" in curItem
            discount = int(offers.find("a").text.replace("SAVE", "").replace("%", "").replace("EXTRA", "").strip())
            # Find "a" in offers, and collect the text from it. Then replace "save" with empty space.
            # Replace "%" into empty space,replace "extra" with empty space. Use strip to clean the empty space,
            # then convert it into interger
        except:  # if discount =0 then except this
            discount = 0

        df = df.append({"name": cur_linkAndName,
                        "prices": price,
                        "offers": discount}, ignore_index=True)

    return df


def searchInfoOnPageAndSaveResults(startingUrl, fileNameToSave):
    arrOfPages = getLinksToNextPages(startingUrl)

    arrFinal = np.array([])
    for itter, curElem in enumerate(arrOfPages):
        eachlink = "https://www.davidjones.com/" + curElem
        arrFinal = np.append(arrFinal, eachlink)

    arrFinal = np.append(arrFinal, startingUrl)

    dataFrame = pd.DataFrame()
    for curUrl in arrFinal:  # curUrl is in listOfUrl

        df = getPrice_ItemName_Discount_fromWebsite(curUrl)  # Call the function
        dataFrame = dataFrame.append(df, ignore_index=True)

    dataFrame.to_csv(fileNameToSave)
    print("Done")


if __name__ == "__main__":
    startingUrl = "https://www.davidjones.com/gifts/gift-by-occasion/house-warming?src=fh&size=90"
    fileNameToSave = f"fulldf.csv"

    searchInfoOnPageAndSaveResults(startingUrl, fileNameToSave)
