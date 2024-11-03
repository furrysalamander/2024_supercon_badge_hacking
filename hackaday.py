import requests
import re
import json

def strip_html(html):
    """
    Strips HTML tags manually without using regular expressions.
    
    :param html: str - The HTML data as a string.
    :return: str - The plain text extracted from the HTML.
    """
    in_tag = False
    text = []
    html = html.replace("’", "'")
    print("stripping an article")
    for char in html:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        else:
            if not in_tag:
                text.append(char)
    print("done with one article")
                
    # Join the list into a single string
    return ''.join(text).replace('&nbsp;', ' ').replace('&amp;', '&').strip()

#     return match.group(1).replace("<br />", "").replace("â\x80\x99", "'").replace("Â\xa0", "\n")

def get_articles():
    print("querying hackaday rss feed")
    r = requests.get("https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fhackaday.com%2Fblog%2Ffeed%2F")

    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request \n" +
                "Response Status: " + str(r.text))
        print(r.status_code)
    else:
        print("Success")
        response_data = json.loads(r.text)
    articles = []
    n = 0
    for item in response_data["items"]:
        n += 1
        if n > 3:
            break
        stripped_text = strip_html(item["content"])
        text = f"{item["title"]}\n{stripped_text}"
        articles.append(text)
    return articles

if __name__=="__main__":
    import utils
    utils.connect_to_wifi()

    for article in get_articles():
        utils.write_to_typewriter(
            article
        )

# from pprint import pprint
# pprint(get_hackaday_articles())
