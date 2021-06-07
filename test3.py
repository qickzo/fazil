from bs4 import BeautifulSoup


html_doc = """
    <html>
    <head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2"><b>Dilshad</b></a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>

    <p class="story">...</p>
"""


def scrap(ps):
    def s(p):
        for child in p.children:
            if type(child) == type(BeautifulSoup('<b><span>Dilshad</span></b>', 'html.parser').b):
                s(child)
            else:
                print('|-->  ', child)
    if type(ps) == type(BeautifulSoup('<b>Dilshad</b>', 'html.parser').find_all('b')):
        for p in ps:
            s(p)
    else:
        print('-->  ', ps)


soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.contents)
ps = soup.find_all('p')
scrap(ps)



