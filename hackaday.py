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


# def strip_html(html):
#     """
#     Extracts plain text from HTML by removing all tags.
    
#     :param html: str - The HTML data as a string.
#     :return: str - The plain text extracted from the HTML.
#     """
#     # Remove HTML tags using a regular expression
#     text = re.sub(r'<[^>]+>', '', html)
#     # Replace HTML entities with actual characters if needed
#     text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
#     # Strip leading/trailing whitespace and return
#     return text.strip()

# def strip_html(text: str):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
#     }
#     payload = f"keep_line_breaks=true&textnonsense={url.encode(text)}"
#     print(payload)
#     return ""
#     payload = {
#         'keep_line_breaks': True,
#         'textnonsense': text
#     }
#     # data_encoded = '&'.join(f"{n}={v}" for n,v in payload.items())

#     print("stripping html api call")
#     r = requests.post('https://striphtml.com/',
#                     headers=headers,
#                     data=payload,
#                 )
    
#     if r.status_code >= 300 or r.status_code < 200:
#         print("There was an error with your request \n" +
#                 "Response Status: " + str(r.text))
#         print(r.status_code)
#     else:
#         print("Success")
#     print("doing regex to scrape plaintext")
#     striphtml_response = r.text.replace("\n", " ")

#     pattern = "<div id=\\'cleantext\\'>(.*?)</div>"
#     # pattern = r"<div id=\'cleantext\'>(.+?)<"

#     # pattern = r"<div id=\\'cleantext\\'>(.+?)<\\/div>"
#     match = re.search(pattern, striphtml_response)
    
#     return match.group(1).replace("<br />", "").replace("â\x80\x99", "'").replace("Â\xa0", "\n")

def get_hackaday_articles():
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

import main
main.connect_to_wifi()

for article in get_hackaday_articles():
    main.write_to_typewriter(
        article
    )

# from pprint import pprint
# pprint(get_hackaday_articles())
