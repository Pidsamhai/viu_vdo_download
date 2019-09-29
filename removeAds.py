from lxml.etree import tostring
import lxml.html
import requests

# take AdRemover code from here:
# https://github.com/buriy/python-readability/issues/43#issuecomment-321174825
# from adremover import AdRemover
from adremove import AdRemover

rule_urls = ['https://raw.githubusercontent.com/easylist-thailand/easylist-thailand/master/subscription/easylist-thailand.txt']

# rule_files = [url.rpartition('/')[-1] for url in rule_urls]

# print(rule_files)

rule_files = ['./adscontent/easylist-thailand.txt',]

# # download files containing rules
# for rule_url, rule_file in zip(rule_urls, rule_files):
#     r = requests.get(rule_url)
#     with open(rule_file, 'w') as f:
#         print(r.text, file=f)

def removeAds(url):
    remover = AdRemover(*rule_files)

    html = requests.get(url).text
    document = lxml.html.document_fromstring(html)
    remover.remove_ads(document)
    clean_html = tostring(document).decode("utf-8")
    return clean_html
    #print(clean_html)