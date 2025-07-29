import requests


def scrape_user_tweets(username: str):
    print(
        f"we should be looking for tweets from {username} but I don't want to connect with x api"
    )

    tweet_list = []
    response = requests.get(
        "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json",
        timeout=10,
    ).json()

    for tweet in response:
        tweet_list.append(
            {
                "text": tweet["text"],
                "url": f"https://twitter.com/{username}/status/{tweet["id"]}",
            }
        )
    return tweet_list
