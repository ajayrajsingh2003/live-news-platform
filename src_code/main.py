import os
from venv import create
from dotenv import load_dotenv
from newYorkAPI import nyt_top_news_us
from processHeadlines import *
from processWords import *
from videoDataAzure import *

def fetch_data(nyt_api_key):

    # Get US Top News
    fetch_ny_news = nyt_top_news_us(nyt_api_key)

    # Get Top Headlines
    headlines = fetch_headlines(fetch_ny_news)

    # Create headline words for wordcloud
    front_end_words = create_word_cloud_words(fetch_ny_news)

    # Calculate word occurrences of descriptions for WordCloud
    word_frequency_dict, wordcloud_words = word_value_calculated(front_end_words, headlines, fetch_ny_news)

    # Calculate real time value of these words and provide the real score
    trend_score = score_all_words(word_frequency_dict) # words values as per real time scoring and in news frequency

    # Create the final json for frontend(wordcloud)
    json_for_wordcloud = {
        'words': front_end_words,
        'frequency of image length': wordcloud_words,
        'scored_words': trend_score
    }

    return json_for_wordcloud,headlines

# function to return news and video data
def video_data_of_headlines(azure_api_key, headlines):
    news_json, videos_json = fetch_news_and_videos(azure_api_key, headlines)
    return news_json, videos_json


# We will confirm API keys here and use them to generate data of wordcloud, news and related videos
if __name__ == "__main__":
    # Load .env from config folder
    dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
    load_dotenv(dotenv_path=dotenv_path)

    # Access API keys
    nyt_api_key = os.getenv("NYT_API_KEY")
    azure_api_key = os.getenv("AZURE_API_KEY")

    # if keys are not working raise error
    if not nyt_api_key or not azure_api_key:
        raise ValueError("API keys are missing. Please check your config/.env file.")

    print("API Keys Loaded Successfully!")

    # Calling to get all the data for wordcloud creation
    json_for_wordcloud, headlines = fetch_data(nyt_api_key)

    # Calling to get all the data on videos.
    json_for_news, json_for_videos  = video_data_of_headlines(azure_api_key, headlines)

