## Extractors

Most of the heavy lifting is done by Goose. The rest of the extractor scaffolding is to get additional metadata out of articles. Like social shares, tags, section, topics, etc.

###Example

Let's import the module and define a url

```python
import extractors as extr

url = "http://www.thehindu.com/sport/cricket/phillip-hughes-dies/article6639119.ece"
```

Custom extractors inherit from the `BaseArticleExtractor` (which does the Goose stuff) and `SocialShares` (which makes api calls) and extend it by adding any properties custom to the newspaper. For example, lets look at The Hindu (a popular daily English newspaper)

```python
>>> article = extr.TheHinduExtractor(url=url)
```

Now the article object has been prepopulated with porperties that could be extracted. Let's look at the properties inherited from the `BaseArticleExtractor` (which uses Goose)

```python
>>> article.title
'Australian cricketer Phil Hughes dies of injuries'

>>> article.text[150]
'Australian cricketer Phillip Hughes died in hospital in Sydney on Thursday, two days after the international batsman was struck on the head by a ball during a domestic match.\n\nGoverning body Cricket A'

>>> article.image
'http://www.thehindu.com/multimedia/dynamic/02221/26TH_HUGHES_2221642f.jpg'
```

The following properties are inherited from the `SocialShares` class, which makes api calls to the various social APIs to find share/like counts of an article.

```python
>>> article.facebook_shares
545

>>> article.twitter_shares
30

>>>article.linkedin_shares
0
```


Now let's look at the newspaper-specific properties we added

```python
>>> article.tags
['Phillip Hughes', 'Phil Hughes', 'cricket accident']

>>> article.topics
[' society', ' death', ' sport', ' cricket']

>>>article.section
'Sport'
```

This was written for to prepare a newspaper dataset, where additional features over those provided by goose were needed.
