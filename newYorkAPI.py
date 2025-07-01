import requests

#NYTIMES all top news
def nyt_top_news_us(nyt_api_key):
    url = "https://api.nytimes.com/svc/topstories/v2/us.json"
    # parameters of API
    params = {
        "api-key": nyt_api_key,
    }
    # Response from API
    response = requests.get(url, params=params)

    # To check working
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []