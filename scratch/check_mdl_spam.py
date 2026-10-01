import urllib.request, urllib.parse, json

title = "MDL-SPAM: A Multi Model Deep Learning Framework"
url = 'https://api.crossref.org/works?query.title=' + urllib.parse.quote(title) + '&select=title,author,published-print,URL&rows=5'
req = urllib.request.Request(url, headers={'User-Agent': 'mailto:test@example.com'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        for item in data['message']['items']:
            authors = [a.get('family', '') + ' ' + a.get('given', '') for a in item.get('author', [])]
            print(f"Found: {item.get('title', [''])[0]}")
            print(f"Authors: {authors}")
            print(f"URL: {item.get('URL', '')}")
            print("-" * 40)
except Exception as e:
    print(f'Error: {e}')
