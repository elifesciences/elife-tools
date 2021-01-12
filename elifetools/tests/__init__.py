def soup_body(soup):
    "extract the main body tag from a BeautifulSoup object"
    return soup.contents[0]
