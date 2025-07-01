import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pytrends.request import TrendReq
import json
import string
import time

# Formula: Final Score = 0.4 * Base Score + 0.6 * Trend Score

#Calculate word frequency for news_description_words
def word_value_calculated(words_per_headline, headlines, result):
    # Setup
    custom_stopwords = set(['said', 'according', 'reported', 'news', 'article', 'time'])
    stop_words = set(stopwords.words('english')).union(custom_stopwords)
    headline_Des_Facet_wordlist = {}

    # --- Build word list per headline ---
    all_words_nested = []
    for data in range(result['num_results']):
        headline_id = 'headline' + str(data + 1)
        headline_Des_Facet_wordlist[headline_id] = []

        content = result['results'][data].get('des_facet', []) or [result['results'][data]['title']]
        all_text = ' '.join(content)
        words = word_tokenize(all_text)
        filtered_words = [
            word.lower().strip(string.punctuation)
            for word in words
            if word.lower().strip(string.punctuation) not in stop_words and word.isalpha()
        ]

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))
        headline_Des_Facet_wordlist[headline_id].append(list(wordcloud.words_.keys()))

        all_words_nested.append(filtered_words)

    # Flatten and count all words
    flat_words = [word for sublist in all_words_nested for word in sublist]

    # Create word cloud and find wordcloud keys

    # Generate final wordcloud
    final_text = ' '.join(flat_words)
    final_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(final_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(final_wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # Calculate the wordcount
    word_count = {}
    for word in flat_words:
        word_count[word] = word_count.get(word, 0) + 1
    print(word_count)
    return word_count, final_wordcloud.words_


# PyTrends Setup and Scoring Functions
def get_trend_score(word):
    pytrends = TrendReq(hl='en-US', tz=360)
    try:
        pytrends.build_payload([word], timeframe='now 1-H')
        time.sleep(1.5) # delay to not kill library frequency
        data = pytrends.interest_over_time()
        if not data.empty:
            latest_value = data[word].iloc[-1]
            return latest_value / 100
        else:
            return 0.0
    except:
        return 0.0

# Calculate base_score, trend_score, final_score
def calculate_final_score(word, word_freq_dict, alpha=0.4, beta=0.6):
    total_count = sum(word_freq_dict.values())
    base_score = word_freq_dict.get(word, 0) / total_count if total_count else 0.0
    trend_score = get_trend_score(word)
    final_score = alpha * base_score + beta * trend_score
    return {
        "word": word,
        "base_score": round(base_score, 4),
        "trend_score": round(trend_score, 4),
        "final_score": round(final_score, 4)
    }

# calculate top 30 words trending Scores
def score_all_words(word_freq_dict, top_n=30):
    scored_words = [calculate_final_score(word, word_freq_dict) for word in word_freq_dict]
    scored_words.sort(key=lambda x: x['final_score'], reverse=True)
    return scored_words[:top_n]