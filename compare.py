from bs4 import BeautifulSoup
import requests, re

class Search:
    
    def __init__(self, query, max_page):
        self.max_page = int(max_page)
        self.query = str(query).lower()
        self.url = f"https://iprice.co.id/search/?term={self.query.replace(' ', '%20')}"
        self.result = []
    
    def request(self):
        head = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Upgrade-Insecure-Request": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666"
        }
        try:
            base_page = 1
            req = requests.get(f"{self.url}&page={base_page}", headers=head)
            while ("Kami tidak menemukan produk yang dicari, periksa ejaan dan filter Anda." not in req.text):
                if base_page > self.max_page:
                    break
                else:
                    soup = BeautifulSoup(req.text, 'html.parser')
                    if soup.find_all('div', attrs={'class': 'pu kF oT cM iq iU iV uu'}) != None:
                        cards = soup.find_all('div', attrs={'class': 'pu kF oT cM iq iU iV uu'})
                        response = self.parse(cards)
                        if response != None:
                            self.result.append(response)
                    else:
                        self.request(self)
                    base_page = base_page + 1
                    req = requests.get(f"{self.url}&page={base_page}", headers=head)
        except Exception as e:
            print("Error Exception:", str(e))
    
    def parse(self, cards):
        for item in cards:
            if item.find('span', attrs={'class': 'truncate-2'}) != None and item.find('span', attrs={'class': 'hF b p bQ a-'}) != None:
                name = item.find('span', attrs={'class': 'truncate-2'}).get_text()
                price = item.find('span', attrs={'class': 'hF b p bQ a-'}).get_text()
                result = {'name': name, 'price': price}
            else:
                result = None
            return result
    def get(self):
        self.request()
        return self.result
                


    