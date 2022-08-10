import sys

from PyQt5.QtCore import QUrl

import bs4 as bs

from PyQt5.QtWebEngineWidgets import QWebEnginePage as QWebPage

from PyQt5.QtWidgets import QApplication


class Client(QWebPage):
    theApp = QApplication(sys.argv)

    def __init__(self, url):
        self.app = Client.theApp
        QWebPage.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        self.app.exec_()

    def _callable(self, data):
        self.html = data

    def _loadFinished(self, result):
        self.toHtml(self.callable)

    def callable(self, data):
        self.html = data
        self.app.quit()


def getHtmlFromUrl(url):
    return Client(url).html


if __name__ == "__main__":
    url = "https://www.davidjones.com/gifts/gift-by-occasion/house-warming?src=fh&size=90&offset=90"
    receivedHtml = Client(url).html
    soup = bs.BeautifulSoup(receivedHtml, 'lxml')
    js_test = soup.find('p', class_='jstest')
    print(js_test.text)
