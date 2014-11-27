import db
import extractors as extr
from slugify import slugify
import os

for story in db.s_coll.find({"title": {'$exists': False}}):

    url = story['url']
    article = extr.TheHinduExtractor(url=url)

    curpath = os.path.abspath(os.curdir)
    yr, mo, day = story['date'].split('/')
    path = os.path.join(curpath, 'data', yr, mo, day)
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, slugify(article.title) + '.txt')
    response_dict = {
        'path'    : filename,
        'title'   : article.title,
        'meta'    : article.meta,
        'image'   : article.image,
        'tags'    : article.tags,
        'topics'  : article.topics,
        'section' : article.section,
        'social_shares': {
                'facebook': article.facebook_shares,
                'twitter' : article.twitter_shares,
        }
    }

    db.s_coll.update(
                     {'_id': story['_id']},
                     response_dict
                    )

    with open(filename, 'w+') as f:
        f.write(article.text)


