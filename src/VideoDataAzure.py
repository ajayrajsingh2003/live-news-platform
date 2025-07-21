import requests

#Fetch News & Videos related to every headline
def fetch_news_and_videos(subscription_key, headlines):
    # creating news and videos jsons for frontend
    news_json = {}
    videos_json = {}
    final_json = {'news': news_json, 'videos': videos_json}

    # news api and videos api
    api_news, api_videos = 'https://api.bing.microsoft.com/v7.0/news/search', 'https://api.bing.microsoft.com/v7.0/videos/search'

    # making a list of api(news, videos)
    endpoints_of_data = [api_news, api_videos]

    for endpoint in range(len(endpoints_of_data)):
        # Running all news first and then getting all the related videos
        # loop for headlines
        for search in range(len(headlines)):

            # Query headline(s) to search for.
            query = headlines[search]

            # Construct a request
            mkt = 'en-US'
            params = {'q': query, 'mkt': mkt}
            headers = {'Ocp-Apim-Subscription-Key': subscription_key}

            # Call the API
            try:
                response = requests.get(endpoints_of_data[endpoint], headers=headers, params=params)
                response.raise_for_status()

                # result from bing API(you can print it to check)
                bing_result = response.json()
                headline_num = search + 1

                # adding data to news (if endpoint = 0) and then videos json (if endpoint = 1)
                # Adding News to json
                if endpoint == 0:
                    news_json['headline' + str(headline_num)] = {}
                    for total_num_news in range(len(bing_result['value'])):
                        news_number = total_num_news + 1
                        news_json['headline' + str(headline_num)]['News' + str(news_number)] = {}

                        # title of news
                        news_json['headline' + str(headline_num)]['News' + str(news_number)]['name'] = \
                        bing_result['value'][total_num_news]['name']

                        # url of news
                        news_json['headline' + str(headline_num)]['News' + str(news_number)]['url'] = \
                        bing_result['value'][total_num_news]['url']

                        # articleImage(thumbnail)
                        try:
                            # Try to access the 'thumbnail' under the 'image' key
                            news_json['headline' + str(headline_num)]['News' + str(news_number)]['thumbnail'] = \
                            bing_result['value'][total_num_news]['image']['thumbnail']['contentUrl']
                        except KeyError:
                            try:
                                # Handle the case when 'image' key or its nested keys do not exist(give source image)
                                news_json['headline' + str(headline_num)]['News' + str(news_number)]['thumbnail'] = \
                                bing_result['value'][total_num_news]['provider'][0]['image']['thumbnail']['contentUrl']
                            except:
                                # Handle the case with organisation's name
                                news_json['headline' + str(headline_num)]['News' + str(news_number)]['thumbnail'] = \
                                bing_result['value'][total_num_news]['provider'][0]['name']

                        # description
                        news_json['headline' + str(headline_num)]['News' + str(news_number)]['description'] = \
                        bing_result['value'][total_num_news]['description']

                        # date of publication
                        news_json['headline' + str(headline_num)]['News' + str(news_number)]['datePublished'] = \
                        bing_result['value'][total_num_news]['datePublished']

                if endpoint == 1:
                    video_number = 0
                    videos_json['headline' + str(headline_num)] = {}
                    for total_num_video in range(len(bing_result['value'])):

                        video_number = total_num_video + 1
                        videos_json['headline' + str(headline_num)]['Video' + str(video_number)] = {}

                        # name
                        videos_json['headline' + str(headline_num)]['Video' + str(video_number)]['name'] = \
                        bing_result['value'][total_num_video]['name']

                        # description
                        try:
                            videos_json['headline' + str(headline_num)]['Video' + str(video_number)]['description'] = \
                            bing_result['value'][total_num_video]['description']
                        except:
                            videos_json['headline' + str(headline_num)]['Video' + str(video_number)][
                                'description'] = 'No Description Available'

                        # thumbnailUrl
                        videos_json['headline' + str(headline_num)]['Video' + str(video_number)]['thumbnailUrl'] = \
                        bing_result['value'][total_num_video]['thumbnailUrl']

                        # datePublish
                        videos_json['headline' + str(headline_num)]['Video' + str(video_number)]['datePublish'] = \
                        bing_result['value'][total_num_video]['thumbnailUrl']

                        # contentUrl
                        videos_json['headline' + str(headline_num)]['Video' + str(video_number)]['contentUrl'] = \
                        bing_result['value'][total_num_video]['contentUrl']
            except Exception as ex:
                raise ex

    return news_json, videos_json