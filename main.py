import pickle
import pandas as pd
import Config
import re
from Event import Event


class NoURLsFoundException(Exception):
    "If there are no URLs"


def search_page_get_urls(page_n=1):
    """
    From the search results page on Eventbrite, this function finds the URLs to all events.
    :param page_n:
    :return:
    """
    import requests
    url = f'https://www.eventbrite.com/d/online/{Config.SEARCH_KEYWORDS}/?page={page_n}&start_date={Config.DATE_RANGE_START}&end_date={Config.DATE_RANGE_END}'
    resp = requests.get(url)
    urls = re.findall('<a tabindex="[0-9]+" href="(.*?)"', resp.text)
    if not urls:
        raise NoURLsFoundException()
    urls = [urls[i] for i in range(len(urls)) if i % 2 == 0]
    return urls


def filter_events(events):
    """
    Naive filter using keywords. Could be replaced by more sophisticated filter.
    :param events:
    :return:
    """
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


def save_as_csv():
    """
    Saves the pickled result to csv. I am doing this two stage process,
    to ensure that results of the lengthy scraping process are always saved to pickle first and are never lost.
    Could of course save as CSV straight away.
    :return:
    """

    with open('eventbrite.pkl', 'rb') as file:
        res = pickle.load(file)

    def events_to_csv(events):
        import pandas as pd
        return pd.DataFrame([[e.date, e.title, e.url] for e in res], columns=['date', 'title', 'url'])

    filename = f'eventbrite_{pd.datetime.now().strftime("%d%m%Y")}.csv'
    events_to_csv(res).to_csv(filename, sep=';')


if __name__ == "__main__":
    res = []
    # Limiting to top 20 result pages, as results become diluted after that
    for i in range(20):
        print(i)
        # Stop searching early if there are no more result pages
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
    save_as_csv()
