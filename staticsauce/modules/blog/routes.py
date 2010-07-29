from staticsauce.routes import RouteMapper
from staticsauce.modules.blog import models


ARTICLES_URL = '/articles'
ARTICLES_FILENAME = '/articles.html'

ARTICLE_URL = '/articles/{article}'
ARTICLE_FILENAME = '/articles/{article}.html'

def mapper():
    mapper = RouteMapper()

    articles = models.articles()
    mapper.add(ARTICLES_URL, ARTICLES_FILENAME,
               template='/blog/articles.html', articles=articles)

    for article in articles:
        url = ARTICLE_URL.format(article=article['slug'])
        filename = ARTICLE_FILENAME.format(article=article['slug'])
        mapper.add(url, filename,
                   template='/blog/article.html', article=article)
    return mapper
