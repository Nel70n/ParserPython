from bs4 import BeautifulSoup, Comment

data = """<div class="foo">
cat dog sheep goat
<!--
<p>test</p>
-->
</div>"""

soup = BeautifulSoup(data, "html.parser")

div = soup.find('div')
for element in soup(text=lambda text: isinstance(text, Comment)):
    element.extract()

print (soup.prettify())