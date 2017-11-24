import urllib.request

def get_page(url):
    try:
        if url == "https://www.rishabhverma.in/index.html":
            return ('<html> <body> This is a test page for learning to crawl! '
            '<p> It is a good idea to '
            '<a href="https://www.rishabhverma.in/crawling.html">learn to '
            'crawl</a> before you try to  '
            '<a href="https://www.rishabhverma.in/walking.html">walk</a> '
            'or  <a href="https://www.rishabhverma.in/flying.html">fly</a>. '
            '</p> </body> </html> ')
        elif url == "https://www.rishabhverma.in/crawling.html":
            return ('<html> <body> I have not learned to crawl yet, but I '
            'am quite good at '
            '<a href="https://www.rishabhverma.in/kicking.html">kicking</a>.'
            '</body> </html>')
        elif url == "https://www.rishabhverma.in/walking.html":
            return ('<html> <body> I cant get enough '
            '<a href="https://www.rishabhverma.in/index.html">crawling</a>! '
            '</body> </html>')
        elif url == "https://www.rishabhverma.in/flying.html":
            return ('<html> <body> The magic words are Squeamish Ossifrage! '
            '</body> </html>')
    except:
        return ""
    return ""

# Get content as text from Web Page.
'''
    --> def get_page_internet(url):
    This procedure Reads the web page from provided URL and return content of web page as text.
    same text as viewed in page source. [with html tags] 
'''
def get_page_internet(url):
    url_read = urllib.request.urlopen(url)
    pw = url_read.read()
    read_line = str(pw)
    return read_line
# Get first links[URL] encountered in HTML Page
'''
    --> def get_next_target(page):
    This procedure takes HTML Page as text input.
    As it encounters the first "<a href=" tag it gets that URL.
    Then it Change the start position of page to index after the first encountered URL.
    Returns the URL and New start Index on that Page. 
'''
def get_next_target(page):
    start_link = page.find("<a href=")
    # Stopping Condition
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_qoute = page.find('"', start_quote+1)
    url = page[start_quote+1:end_qoute]
    return url, end_qoute

# Appends URL in Crawled List from to_crawl List.
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

'''
    --> def get_all_links(page):
    Returns all the URL present in page and stores in links_list[].
'''
def get_all_links(page):
    # Stores all the URL of passed HTML[seed page] page.
    links_list = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            # add links to List
            links_list.append(url)
            # Start page from new Index.
            # New Index is after the last encountered URL.
            page = page[endpos:]
        else:
            break
    return links_list

# Data Structure using here is : Multimap
'''
    index[] --> [keyword, [URL]] :Single Keyword multiple URL's
    If we found an existing keyword of passed URL and Keyword in Index[] list then URL will be appended to that list.
    If not found the we will append new list consisting --> [keyword, [URL]]
'''
def add_to_index(index, keyword, url):
    for entry in index:
        # Search for existence of passes keyword in list Index[].
        if entry[0] == keyword:
            # If Keyword exist, then append URL to that list.
            entry[1].append(url)
            return
    # If not keyword not found then add new list with Keyword and URL.
    index.append([keyword, [url]])

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

'''
    # The procedure returns a list of the urls associated with the keyword.
    # If the keyword is not in the index, the procedure returns an empty list.
'''
def lookup(index,keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
        return []

# Seed Page[HTML page which needs to be crawled] is passed as input. Returns all the crawled links.
# max_pages -> to set maximum number of pages that will be crawled.
def crawl_web(seed,max_pages):
    # HTML pages to be crawled
    tocrawl = [seed]
    # HTML Pages crawled
    crawled = []
    index = []
    while tocrawl:
        # Returns last URL in tocrawl list and Removes it from tocrawl List.
        last_url = tocrawl.pop()
        # If provided URL is not already crawled previously.
        if last_url not in crawled:
            content = get_page_internet(last_url)
            add_page_to_index(index, last_url, content)
            # uncomment this to crawl sample pages provided in script[to test without internet connection]
            #union(tocrawl, get_all_links(get_page(last_url)))
            union(tocrawl, get_all_links(get_page_internet(last_url)))
            crawled.append(last_url)
    return index

print (crawl_web("https://www.rishabhverma.in/webCrawling/index.html",5))

#print (crawl_web("https://www.rishabhverma.in/index.html",3))
#print(get_page("https://www.rishabhverma.in/index.html"))
#print(get_page_internet("https://www.rishabhverma.in/webCrawling/"))
