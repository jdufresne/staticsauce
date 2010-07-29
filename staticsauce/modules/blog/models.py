import os
import errno
from staticsauce import config

def articles():
    articles = []
    dirname = os.path.join(config.get('project', 'data_dir'), 'blog')

    try:
        filenames = os.listdir(dirname)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e
    else:
        for filename in filenames:
            document = minidom.parse(os.path.join(dirname, filename))
            article = Article(slug_from_filename(filename),
                              get_element_text(document, 'title'),
                              get_element_text(document, 'author'),
                              get_element_text(document, 'date'),
                              get_element_text(document, 'content'))
            articles.append(article)
    return articles

class Article:
    def __init__(self, slug, title, author, date, content):
        self.slug = slug
        self.title = title
        self.author = author
        self.date = date
        self.content = content
