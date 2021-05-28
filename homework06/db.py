from scraputils import get_news

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)


def add_data(obj, url, n_pages):
    data = get_news(url, n_pages)
    for i in data:
        news = News(title=i['title'],
                    author=i['author'],
                    url=i['url'],
                    comments=i['comments'],
                    points=i['points'])
        obj.add(news)
    obj.commit()


s = session()
add_data(s, "https://news.ycombinator.com/", 26)
