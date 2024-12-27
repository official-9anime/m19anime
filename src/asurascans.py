from bs4 import BeautifulSoup
import requests

class Asurascans:
    def __init__(self) -> None:
        self.proxy_url = "https://cdn.aniwave.lat/"
        self.parent_url = "https://asurascans.io"
        self.results = {
            "status": "",
            "results": []
        }

    def fetch_html(self, url):
        try:
            response = requests.get(f"{self.proxy_url}{url}")
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.results["status"] = "error"
            self.results["results"] = str(e)
            return None

    def search(self, query: str):
        try:
            url = f"{self.parent_url}/?s={query}"
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            cards = soup.select("#content > div > div.postbody > div > div.listupd > div > div.bsx")
            content = []

            for items in cards:
                tempContent = {}
                tempContent["title"] = items.find("a").get("title")
                tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
                tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("src")
                tempContent["chapters"] = items.find("div", class_="epxs").get_text()
                content.append(tempContent)

            self.results["results"].append(content)
            return self.results
        except Exception as e:
            self.results["results"] = str(e)
            return self.results

    def info(self, id: str):
        try:
            url = f"{self.parent_url}/manga/{id}"
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            content = {}
            content["images"] = soup.select_one("div.seriestucon > div.seriestucontent > div.seriestucontl > div.thumb > img").get("data-src")
            content["description"] = soup.select_one("div.seriestucon > div.seriestucontent > div.seriestucontentr > div.seriestuhead > div.entry-content.entry-content-single > p").get_text()

            infoSelector = soup.select_one("div.seriestucon > div.seriestucontent > div.seriestucontentr > div.seriestucont > div > table > tbody")
            content["status"] = infoSelector.select_one("tr:nth-child(1) > td:nth-child(2)").get_text()
            content["type"] = infoSelector.select_one("tr:nth-child(2) > td:nth-child(2)").get_text()
            content["year"] = infoSelector.select_one("tr:nth-child(3) > td:nth-child(2)").get_text()
            content["author"] = infoSelector.select_one("tr:nth-child(4) > td:nth-child(2)").get_text().split(",")
            content["artists"] = infoSelector.select_one("tr:nth-child(5) > td:nth-child(2)").get_text().split(",")
            content["serialization"] = infoSelector.select_one("tr:nth-child(6) > td:nth-child(2)").get_text().split(",")

            genresSelector = soup.select("div.seriestucon > div.seriestucontent > div.seriestucontentr > div.seriestucont > div > div > a")
            content["genres"] = ", ".join(i.get_text() for i in genresSelector)

            chapterSelector = soup.select("#chapterlist > ul > li > div > div")
            chapters = []
            for items in chapterSelector:
                tempChapter = {}
                tempChapter["title"] = items.find("span", class_="chapternum").get_text()
                tempChapter["date"] = items.find("span", class_="chapterdate").get_text()
                tempChapter["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
                chapters.append(tempChapter)
            content["chapters"] = chapters

            self.results["results"].append(content)
            return self.results
        except Exception as e:
            self.results["results"] = str(e)
            return self.results

    def pages(self, id: str):
        try:
            url = f"{self.parent_url}/{id}"
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            imgSelector = soup.select("#readerarea > p > img")
            self.results["results"] = [i.get("data-src") for i in imgSelector]
            return self.results

        except Exception as e:
            self.results["results"] = str(e)
            return self.results

    def popular(self):
        try:
            url = self.parent_url
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            cards = soup.select("#content > div > div.hotslid > div > div.listupd.popularslider > div > div > div.bsx")
            content = []

            for items in cards:
                tempContent = {}
                tempContent["title"] = items.find("a").get("title")
                tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
                tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("data-src")
                tempContent["chapters"] = items.find("div", class_="epxs").get_text()
                content.append(tempContent)

            self.results["results"].append(content)
            return self.results
        except Exception as e:
            self.results["results"] = str(e)
            return self.results

    def latest(self, page: str = "1"):
        try:
            url = f"{self.parent_url}/manga/?page={page}&order=update"
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            cards = soup.select("#content > div > div.postbody > div.bixbox.seriesearch > div.mrgn > div.listupd > div > div.bsx")
            content = []

            for items in cards:
                tempContent = {}
                tempContent["title"] = items.find("a").get("title")
                tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
                tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("data-src")
                tempContent["chapters"] = items.find("div", class_="epxs").get_text()
                content.append(tempContent)

            self.results["results"].append(content)
            return self.results
        except Exception as e:
            self.results["results"] = str(e)
            return self.results

    def genres(self, type: str):
        try:
            url = f"{self.parent_url}/genres/{type}"
            html_content = self.fetch_html(url)
            if not html_content:
                return self.results

            soup = BeautifulSoup(html_content, "html.parser")

            cards = soup.select("#content > div > div > div > div.listupd > div > div.bsx")
            content = []

            for items in cards:
                tempContent = {}
                tempContent["title"] = items.find("a").get("title")
                tempContent["id"] = items.find("a").get("href").rsplit("/", 2)[-2]
                tempContent["image"] = items.find("img", class_="ts-post-image wp-post-image attachment-medium size-medium").get("data-src")
                tempContent["chapters"] = items.find("div", class_="epxs").get_text()
                content.append(tempContent)

            self.results["results"].append(content)
            return self.results
        except Exception as e:
            self.results["results"] = str(e)
            return self.results
