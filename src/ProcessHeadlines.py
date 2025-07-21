from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

url_filter = [] # all urls
headlines = [] # all headlines

def fetch_headlines(result):
    #fetch all urls and titles(run title in bing)
    for parse_URL in range(result['num_results']):

        # Fetching URLS (Top NYTimes headlines) for future enhancements
        article_Url = ''
        article_Url = result['results'][parse_URL]['url']
        url_filter.append(article_Url)

        #Fetching Title
        title = result['results'][parse_URL]['title']
        headlines.append(title)

    # Only returning headlines
    return headlines


# Create a descriptions if not available
def generate_description(news_title):
    pass

# Get Valid Data for wordcloud
def create_word_cloud_words(result):

    # create json for frontend
    headline_des_wordlist = {}

    headline_topic_num = 0
    for data in range(result['num_results']):
        headline_topic_num = data + 1

        # creating list that keep wordcloud word for headlines
        headline_des_wordlist['headline' + str(headline_topic_num)] = []

        # If description doesn't exist, Use title and generate description and add to headline
        if len(result['results'][data]['des_facet']) > 0:
            headline_des_wordlist['headline' + str(headline_topic_num)].append(result['results'][data]['des_facet'])
        else:
            # Use title and fetch description from generate_description function
            # I will use the created function ,and It will make sure that I have a description made from the news title
            headline_des_wordlist['headline' + str(headline_topic_num)].append(generate_description(result['results'][data]['title']))
    return headline_des_wordlist