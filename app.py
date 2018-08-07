import os
from flask import Flask, render_template, request, jsonify
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.search.websearch import WebSearchAPI
from page_reader import PageReader


app = Flask(__name__)

SUBSCRIPTION_KEY = os.environ.get("SUBSCRIPTION_KEY", "")
client = WebSearchAPI(CognitiveServicesCredentials(SUBSCRIPTION_KEY))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def page_to_dict(page):
    return {
        "title": page.name,
        "url": page.url,
        "description": page.snippet,
        "date": page.date_last_crawled
    }


@app.route("/search", methods=["POST"])
def search():
    content = request.get_json()
    query = content["query"]

    # Get search results
    response = client.web.search(query=query)
    """
    Response format is following.
    https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/
    """

    # Get web_page information
    pages = []
    count = 0
    if response.web_pages.value:
        count = response.web_pages.total_estimated_matches
        pages = [p for p in response.web_pages.value]
        pages = [page_to_dict(p) for p in pages]

    search_result = {
        "count": count,
        "pages": pages
    }
    return jsonify(search_result)

@app.route("/detail", methods=["POST"])
def detail():
    content = request.get_json()
    url = content["url"]
    description = content["description"]

    reader = PageReader()
    texts = reader.get_page_text(url, description)

    detail = {
        "detail": {
            "body": texts,
            "words": []
        }
    }
    return jsonify(detail)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
