import sys
from html.parser import HTMLParser
import urllib.request
import urllib.parse
import webbrowser


class Link:
    def __init__(self, title, href):
        self.href = href
        self.title = title


def get_html_attr(attrs, name):
    for attr in attrs:
        if attr[0] == name:
            return attr[1]


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_link = None
        self.record = False
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            if get_html_attr(attrs, "id") == "search":
                self.record = True
        if self.record:
            if tag == "a":
                self.current_link = get_html_attr(attrs, "href")

    def handle_endtag(self, tag):
        if self.record:
            if tag == "a":
                self.current_link = None

    def handle_data(self, text):
        if self.record:
            if self.current_link is not None:
                for link in self.links:
                    if link.href == self.current_link:
                        return

                if self.current_link.startswith("http"):
                    self.links.append(Link(text, self.current_link))


def check_num(goto, num_links):
    if not goto.isdigit():
        print("Please enter a number.")
        return False

    num = int(goto) - 1
    if num >= num_links or num < 0:
        print(f"Please enter a number between 1 and {num_links}")
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = input("Enter search query: ")
    query = urllib.parse.quote(query, safe="")
    print("Searching...")

    request = urllib.request.Request(
        "https://www.google.com/search?q=" + query,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
    )

    parser = MyHTMLParser()
    with urllib.request.urlopen(request) as data:
        parser.feed(data.read().decode("utf-8"))

        num_links = len(parser.links)

        for i, link in enumerate(parser.links):
            print(f"{i + 1}. {link.title} ({link.href})")

        goto = input("Select link to go to: ")
        while goto:
            if check_num(goto, num_links):
                webbrowser.open(parser.links[int(goto) - 1].href)
            goto = input("Select link to go to: ")
