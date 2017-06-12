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

You can find the related presentation on [Slideshare](https://www.slideshare.net/GeorgeAdrianMunteanu/sentiment-analysis-76862564).

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


## Running

### Collection of the data

In order to properly collect the data, we suggest to set the following contab entries.

```
0 */6 * * * /usr/bin/env python collect_news.py >/dev/null 2>&1
0 */6 * * * /usr/bin/env python collect_tweets.py >/dev/null 2>&1
0 */6 * * * /usr/bin/env python preprocess.py >/dev/null 2>&1
```

In alternative execute manually the scripts.
A time interval of 6 hours is recommended.

### Search Engine & Pearson Correlation

To run the Search Engine or the Pearson Correlation scripts, first setup the environment with the command:

```sh
python setup.py
```
The script ```setup.py```will create the inverted index from the tweets file (previously collected).

Now, you can run the Search Engine to manually find similar tweets to a given query: 

```sh
python SearchEngine.py
```

The web interface will open in your default browser.

Instead, if want to use the Pearson Correlation script, use the following command:

```sh
python PearsonCorrelation.py
```

