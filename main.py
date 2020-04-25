import pickle
import sys

import Config
import re
from Event import Event


class NoURLsFoundException(Exception):
    "If there are no URLs"


def search_page_get_urls(page_n=1):
    import requests
    url = f'https://www.eventbrite.com/d/online/{Config.SEARCH_KEYWORDS}/?page={page_n}&start_date={Config.DATE_RANGE_START}&end_date={Config.DATE_RANGE_END}'
    resp = requests.get(url)
    urls = re.findall('<a tabindex="[0-9]+" href="(.*?)"', resp.text)
    if not urls:
        raise NoURLsFoundException()
    urls = [urls[i] for i in range(len(urls)) if i % 2 == 0]
    return urls


def filter_events(events):
    res = []
    for event in events:
        keyword_count = 0
        for word in Config.FILTER_KEYWORDS:
            keyword_count += event.html.lower().count(word)
        if keyword_count >= 2:
            res.append(event)
    return res


def get_events_by_searchpage(page):
    return [Event(url) for url in search_page_get_urls(page)]



if __name__ == "__main__":
    res = []
    for i in range(1000):
        print(i)
        try:
            events = get_events_by_searchpage(i)
        except:
            events = None
            break

        for event in events:
            event.download_html()
            event.extract_date()
            event.extract_title()
            event.extract_description()

        events = filter_events(events)
        res.extend(events)
    with open('eventbrite.pkl', 'wb') as file:
        pickle.dump(res, file)
