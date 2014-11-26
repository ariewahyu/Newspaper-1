from functools import wraps
from goose import Goose
from lxml import html as lh
import requests
import ujson as json


class WebStuffHandler(object):

    def __init__(self, url):
        self.url = url

    def _retry(max_tries):
        def decorator(func):
            @wraps(func)
            def wrapped(self, *args, **kawrgs):
                tries = 0
                while tries < max_tries:
                    res = func(self, *args, **kawrgs)
                    if res:
                        break
                    print "Retrying"
                    tries += 1
                return res
            return wrapped
        return decorator

    @_retry(max_tries=3)
    def _get_resp(self, url):
        try:
            resp = requests.get(url)
            if not resp.status_code == requests.codes.ok:
                return None
        except requests.exceptions.RequestException:
            """ToDo: should think of something better than
            catching the base exception as a blanket 
            case. Need to know if its a ConnectionError
            (network is slow) or something else"""
            return None
        return resp.text

    @property
    def raw_html(self):
        return self._get_resp(self.url)

    @raw_html.setter
    def raw_html(self, *args, **kwargs):
        raise ValueError("cannot set this property")


class SocialShares(WebStuffHandler):
    """ToDo: Reddit, Pinterest"""

    def __init__(self, *args, **kwargs):

        super(SocialShares, self).__init__(*args, **kwargs)
        self.facebook_shares = self._facebook_shares()
        self.twitter_shares = self._twitter_shares()
        self.linkedin_shares = self._linkedin_shares()

    def _get_count_from_resp(self, uri, key):
        r = self._get_resp(uri)
        resp = json.loads(r)
        if not key in resp:
            return None
        return resp[key]

    def _facebook_shares(self):
        uri = 'http://graph.facebook.com/?id=' + self.url
        key = 'shares'
        return self._get_count_from_resp(uri, key)

    def _twitter_shares(self):
        uri = 'http://urls.api.twitter.com/1/urls/count.json?url=' + self.url
        key = 'count'
        return self._get_count_from_resp(uri, key)

    def _linkedin_shares(self):
        uri = 'http://www.linkedin.com/countserv/count/share?url={}&format=json'
        uri = uri.format(self.url)
        key = 'count'
        return self._get_count_from_resp(uri, key)


class BaseArticleExtractor(WebStuffHandler):

    def __init__(self, *args, **kwargs):
        super(BaseArticleExtractor, self).__init__(*args, **kwargs)
        self._extr = self.extractor()

    def _sanity_check(func):
            def wrapped(self, *args):
                res = func(self, *args)
                for attr in ('title','meta_description','cleaned_text'):
                    assert hasattr(res, attr), \
                        "Extractor object must have {} attribute".format(attr)
                return res
            return wrapped

    @_sanity_check
    def extractor(self):
        """Goose is the default extractor.
        Important: When overrriding remember
        to return an object with attributes
        title, meta and cleaned_text. Else
        sanity check will fail"""
        return Goose().extract(raw_html=self.raw_html)

    @property
    def title(self):
        return self._extr.title

    @property
    def text(self):
        return self._extr.cleaned_text

    @property
    def meta(self):
        return self._extr.meta_description

    @property
    def image(self):
        return self._extr.top_image.src


class TheHinduExtractor(BaseArticleExtractor, SocialShares):

    def __init__(self, *args, **kwargs):
        super(TheHinduExtractor, self).__init__(*args, **kwargs)
        self.__tree = lh.fromstring(self.raw_html)

    @property
    def tags(self):
        return self.__tree.xpath("//div[@id='articleKeywords']/p/a/text()")

    @property
    def section(self):
        return self.__tree.xpath("//h3[@class='artbcrumb']/a/text()")[0]

    @property
    def topics(self):
        return self.__tree.xpath('//h3[@class="cat"]/a/text()')


class IndianExpressExtractor(BaseArticleExtractor, SocialShares):

    def __init__(self, url):
        if url[-1] == '/':
            #to get unpaginated page
            url += '99'
        else:
            url += '/99'

        super(IndianExpressExtractor, self).__init__(url)
        self.__tree = lh.fromstring(self.raw_html)

    @property
    def tags(self):
        return self.__tree.xpath('//a[starts-with(@href,"/tag/")]/text()')

    @property
    def section(self):
        return self.__tree.xpath('//li[@class="first"]/a/text()')


class TimesOfIndiaExtractor(BaseArticleExtractor, SocialShares):

    def __init__(self, *args, **kwargs):
        super(TimesOfIndiaExtractor, self).__init__(*args, **kwargs)
        self.__tree = lh.fromstring(self.raw_html)

    @property
    def tags(self):
        return self.__tree.xpath('//div[@class="read_more"]/a/text()')

    @property
    def section(self):
        return self.__tree.xpath('//div[@class="bdcrumb"]/text()')[1][3:]
