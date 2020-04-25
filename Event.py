import pickle
import re

import requests

class Event:
    html = None
    title = None
    date = None
    description = None

    def __init__(self, url):
        self.url = url

    def download_html(self):
        resp = requests.get(self.url)
        self.html = resp.text

    def extract_date(self):
        day = re.findall('<p class="listing-hero-image--day">([0-9]+)</p>', self.html)
        month = re.findall('<p class="listing-hero-image--month">(.*?)</p>', self.html)
        self.date = f'{day[0]} {month[0]}' if day and month else None

    def extract_title(self):
        title = re.findall('<h1 class="listing-hero-title" data-automation="listing-title">(.*?)</h1>', self.html)
        self.title = title[0] if title else None

    def to_tuple(self):
        pass

    def __repr__(self):
        res = ""
        res += f'title: {self.title}\n'
        res += f'date: {self.date}\n'
        res += f'url: {self.url}\n'
        res += f'description: {self.description}\n'
        return res

    def extract_description(self):
        import bs4
        html_class = 'structured-content-rich-text'
        bs4_object = bs4.BeautifulSoup(self.html, "html.parser").find('div', attrs={'class':html_class})
        self.description = bs4_object.text if bs4_object else None


# e = Event('https://www.eventbrite.com/e/hackcovid-weekly-anti-coronavirus-online-hackathon-tickets-101126405802?aff=ebdssbonlinesearch')
# e.download_html()
if __name__=='__main__':
    with open('event.pkl', 'rb') as file:
        e = pickle.load(file)
    e.extract_title()
    e.extract_date()
    e.extract_description()
    print(e)
