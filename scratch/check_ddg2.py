import urllib.request, urllib.parse
from html.parser import HTMLParser

class DDGParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_result = False
        self.text = []
    
    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

title = '+"MDL-SPAM" +"Multimedia Tools and Applications"'
url = 'https://lite.duckduckgo.com/lite/'
data = urllib.parse.urlencode({'q': title}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        parser = DDGParser()
        parser.feed(html)
        print("\n".join(parser.text[:40]))
except Exception as e:
    print(f'Error: {e}')
