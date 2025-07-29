import os
import requests

mock_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
scrapin_api_endpoint = "https://api.scrapin.io/v1/enrichment/profile"


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        response = requests.get(url=mock_url, timeout=10)
    else:
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }

        response = requests.get(url=scrapin_api_endpoint, params=params, timeout=10)

    data = response.json().get("person")

    # remove empty fields in the payload to reduce token size
    # if not able to meet token limit and to reduce cost

    if data is None:
        return ""

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile("dummy_url", mock=True))
