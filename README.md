SentiCheNews
=============

> A tool for analyzing possible relationships between news and tweet sentiments.

**Sapienza, University of Rome**

*Master of Science in Engineering in Computer Science*

[*Data Mining* class, Fall 2016](http://aris.me/index.php/data-mining-2016)

Project made with ❤ by:

- [Simone Santacroce](https://it.linkedin.com/in/simone-santacroce-272739134)
- [Manuel Coppotelli](https://it.linkedin.com/in/manuelcoppotelli)
- [George Adrian Munteanu](https://it.linkedin.com/in/george-adrian-munteanu-707744134)

You can find the related presentation on [Slideshare](https://www.slideshare.net/ManuelCoppotelli/sentichenews-sentiment-analysis-on-newspapers-and-tweets).

You can find the related tutorial on [YouTube](https://www.youtube.com/watch?v=W7kKXKE2EL8).

---

## Install instruction

Install python packages:

```sh
pip install -r requirements.txt --user
python -c "import nltk; nltk.download('stopwords')"
cp config.py.example config.py
```

Edit the `config.py` file by adding you [Twitter API key](https://apps.twitter.com/); if you want you can also customize the other parameters.

### Dev dependencies

In order to modify the web-app interface, it is necessary to install the proper javascript modules and re-compile the sources:

```sh
npm install
npm run prod
```


## Running


### Dashboard

To launch the dashboard web application simply run the command:

```sh
python dashboard.py
```

The webapp will open in your default browser.


### Collection of the data

In order to properly collect the data, we suggest to set the following contab entries.

```
0 */6 * * * /usr/bin/env python collect_news.py >/dev/null 2>&1
0 */6 * * * /usr/bin/env python collect_tweets.py >/dev/null 2>&1
0 */6 * * * /usr/bin/env python preprocess.py >/dev/null 2>&1
```

In alternative execute manually the scripts.
A time interval of 6 hours is recommended.
