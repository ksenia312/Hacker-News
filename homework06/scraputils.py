import requests
from bs4 import BeautifulSoup
from pprint import pprint


def extract_news(parser):
    news_list, count = [], 1
    string = str(parser.table)
    element = str(count) + ".</span></td>"
    pNumber = string.find(element)
    while pNumber != -1:
        finish = string.find(str(count + 1) + ".</span></td>") \
            if string.find(str(count + 1) + ".</span></td>") != -1 else -1

        page = parser.table.__str__()[pNumber:finish]
        count += 1

        https = page.find('href="https')
        if https != -1:
            border = https + page[https:].find('"', 6)
            url = (page[https:border])[6:]
        else:
            url = 'No url'
            border = page.find('item?id')
        page = page[border:]
        title = page[page.find('>') + 1: page.find('</a>')]
        page = page[page.find('</a>'):]
        point = page.find(' point')
        points = page[page[:point].rfind('">') + 2: point] if point != -1 else '0'
        page = page[point:] if point != -1 else page
        userId = page.find("user?id=")
        if userId != -1:
            userId = userId + 8
            finish = page[userId:].find('"') + userId
            author = page[userId:finish]
            page = page[finish:]
        else:
            author = 'No author'

        comment = page.find("comment")
        comments = page[page[:comment].rfind('>') + 1:comment - 1] if comment != -1 else '0'
        news_list.append(
            {'author': author, 'comments': comments, 'points': points, 'title': title, 'url': url}
        )
        element = str(count) + ".</span></td>"
        pNumber = string.find(element)
    return news_list


def extract_next_page(parser):
    next_page = str(parser.table)[str(parser.table).find("news?p"):]
    next_page = next_page[:next_page.find('"')]
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    trying = get_news("https://news.ycombinator.com", 2)
    pprint(trying)
