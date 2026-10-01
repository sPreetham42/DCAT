import urllib.request, urllib.parse, json

def check_title(title):
    url = 'https://api.crossref.org/works?query.title=' + urllib.parse.quote(title) + '&select=title,author,published-print,URL&rows=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data['message']['items']:
                item = data['message']['items'][0]
                authors = [a.get('family', '') + ' ' + a.get('given', '') for a in item.get('author', [])]
                print(f"Searched: {title}")
                print(f"Found: {item.get('title', [''])[0]}")
                print(f"Authors: {authors}")
                print("-" * 40)
            else:
                print(f'Not found: {title}')
    except Exception as e:
        print(f'Error on {title}: {e}')

titles = [
    "MDL-SPAM: A Multi Model Deep Learning Framework for Email Spam Detection Using VGG-16 and LSTM",
    "A review of spam email detection: analysis of spammer strategies and the dataset shift problem",
    "Smsad: a framework for spam message and spam account detection",
    "Image spam analysis and detection"
]

for t in titles:
    check_title(t)
