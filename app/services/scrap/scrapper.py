import requests
from bs4 import BeautifulSoup
import json

class Scrapper:

    def scrap(self):
        url = "https://pt.aliexpress.com/w/wholesale-ropas-de-mulheres.html?spm=a2g0o.tm1000001720.1000002.0&initiative_id=SB_20230504140629"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        produtos = []
        for item in soup.find_all("div", class_="item"):
            descricao = item.find("div", class_="item-title-wrap").text.strip()
            preco = item.find("span", class_="price-current").text.strip()
            imagem = item.find("img", class_="picCore").get("src")
            produtos.append({
                "descricao": descricao,
                "preco": preco,
                "imagem": imagem
            })

        with open("produtos.json", "w") as outfile:
            json.dump(produtos, outfile)
