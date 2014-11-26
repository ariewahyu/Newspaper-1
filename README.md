## Extractors

Most of the heavy lifting is done by Goose. The rest of the extractor scaffolding is to get additional metadata out of articles. Like social shares, tags, section, topics, etc.

Example

```python
import extractors as extr

url="http://www.thehindu.com/data/sanskrit-and-english-theres-no-competition/article6630269.ece"
```

Custom extractors inherit from the BaseArticleExtractor (which does the Goose stuff) and SocialShares (which makes api calls) and extend it by adding any properties custom to the newspaper. For example, lets look at The Hindu (a popular daily English newspaper)

```python
>>> article = extr.TheHinduExtractor(url=url)

>>> article.text # full text from goose, can write your own to override

>>> article.tags
['Sanskrit', 'English']

>>> article.topics
['politics']

>>> article.facebook_shares
99

>> article.twitter_shares
116
```

This was written for a crawler to prepare a dataset, where additional metadata over that provided by goose was needed.
