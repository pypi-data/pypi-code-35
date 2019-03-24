#! /usr/bin/env python
"""
    Some inspiration from
    https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
"""

import os
import re
import requests
import urllib.parse

from slugify import slugify

from bs4 import BeautifulSoup

class BookstackAPI:
    """
    This is used to manage a connection to a Bookstack Web App
    """

    def __is_downloadable(self, url):
        """ internal method to determine if the link is downloadable or not """

        head_req = self.session.head(url, allow_redirects=True)
        head_req.raise_for_status()

        if 'text' in head_req.headers.get('content-type').lower():
            return False

        if 'html' in head_req.headers.get('content-type').lower():
            return False

        return True

    def __download_file(self, url, destination_dir):
        """ actually download the file """

        file_req = self.session.get(url, allow_redirects=True)
        file_req.raise_for_status()

        filename = re.search(
            r"filename=\"(.+)\"",
            file_req.headers.get('content-disposition'),
        )

        destination_file = os.path.join(destination_dir, filename.group(1))

        open(destination_file, 'wb').write(file_req.content)

    def __extract_token(self, html_text):
        """
        This is used to scan the main page and extract the form token
        before logging in.
        """

        match = re.search(
            r"<input\stype=\"hidden\"\sname=\"_token\"\svalue=\"(\w+)\">",
            html_text,
        )

        if match:
            return match.groups()[0]
        else:
            return None

    def __get_session(self):
        """ do the login, create requests session """

        book_sess = requests.Session()
        token_resp = book_sess.get(self.url)
        token_resp.raise_for_status()
        my_token = self.__extract_token(token_resp.text)

        login_resp = book_sess.post(
            urllib.parse.urljoin(self.url, "login"),
            data = {
                "email": self.user_email,
                "password": self.user_pass,
                "_token": my_token,
            },
        )
        login_resp.raise_for_status()

        self.session = book_sess

    def export_page(self, url, destination_dir):
        """
        This will download a given url to the specified destination directory.
        The file is saved using the filename provided by the web service.
        """

        if self.file_type in ["html", "pdf", "plaintext"]:
            dl_suffix = self.file_type
        else:
            dl_suffix = "html"

        dl_url = f"{url}/export/{dl_suffix}"

        if not self.session:
            self.__get_session()

        if self.__is_downloadable(dl_url):
            self.__download_file(dl_url, destination_dir)
        else:
            print("not downloadable")

    def get_all_books(self):
        """
        This will begin the process of crawling all books, chapters, and pages,
        gathering meta data.
        It will store this information as the books class attribute in a complex
        dictionary format.
        This does not actually download anything.
        This delegates the book crawling work to internal methods.
        """

        # start a session if we don't already have one
        if not self.session:
            self.__get_session()

        # check books url
        books_url = f"{self.url}/books/"
        books_req = self.session.get(books_url)
        books_req.raise_for_status()

        # search through the html
        soup = BeautifulSoup(books_req.content, "html.parser")
        main_div = soup.find("div", class_="container small")
        for this_book in main_div.find_all("a", class_="text-book entity-list-item-link"):
            
            # strip out book name text
            this_book_name = this_book.get_text().strip()

            if self.verbose:
                print(f"Found book '{this_book_name}' at '{this_book['href']}'.")

            # insert into class attribute if it doesn't exist.
            if this_book_name not in self.books.keys():
                self.books[this_book.get_text().strip()] = {
                    'url': this_book['href'],
                    'chapters': {},
                    'pages': [],
                }
            
            self.__get_book_children(this_book_name)

    def __get_book_children(self, book_name):
        """
        This will get meta data for all immediate children in a book including
        all chapters and non-chaptered pages.
        This does not gather data for chaptered pages.  It delegates this work
        to method __get_chapter_pages.
        """

        # start a session if it doesn't exist.
        if not self.session:
            self.__get_session()

        # check chapter url
        book_url = self.books[book_name]['url']
        book_req = self.session.get(book_url)
        book_req.raise_for_status()

        # search through html
        soup = BeautifulSoup(book_req.content, "html.parser")

        for this_chapter in soup.find_all("a", class_="text-chapter entity-list-item-link"):

            this_chapter_name = this_chapter.get_text().strip()

            if self.verbose:
                print(f"Found chapter '{this_chapter_name}' at '{this_chapter['href']}'.")

            if this_chapter_name not in self.books[book_name]['chapters'].keys():
                self.books[book_name]['chapters'][this_chapter_name] = this_chapter['href']

            self.__get_chapter_pages(book_name, this_chapter_name)

        for this_page in soup.find_all("a", class_="text-page entity-list-item-link"):

            this_page_name = this_page.get_text().strip()
            if self.verbose:
                print(f"Found unchaptered page '{this_page_name}' at '{this_page['href']}'.")

            self.books[book_name]['pages'].append({
                "name": this_page_name,
                "chapter": None,
                "url": this_page['href'],
            })
            
    def __get_chapter_pages(self, book_name, chapter_name):
        """
        This will gather meta data for all chaptered pages.
        """
        # start a session if it doesn't exist.
        if not self.session:
            self.__get_session()

        # check chapter url
        chapter_url = self.books[book_name]['chapters'][chapter_name]
        chapter_req = self.session.get(chapter_url)
        chapter_req.raise_for_status()

        # search through html
        soup = BeautifulSoup(chapter_req.content, "html.parser")
        for this_page in soup.find_all("a", class_="text-page entity-list-item-link"):

            this_page_name = this_page.get_text().strip()
            if self.verbose:
                print(f"Found chaptered page '{this_page_name}' at '{this_page['href']}'.")
            
            self.books[book_name]['pages'].append({
                "name": this_page_name,
                "chapter": chapter_name,
                "url": this_page['href'],
            })


    def download_all(self, destination_dir):
        """
        This will download exported pages for everything that has been gathered
        in the book class attribute.
        The pages are stored in a heirarchy under the destination directory specified.
        This can store in html (default), pdf, or plaintext, which is configured on class init. 
        """

        if not self.session:
            self.__get_session()

        for this_book in self.books.keys():

            book_dirname = slugify(this_book)

            for this_page in self.books[this_book]['pages']:

                if this_page['chapter']:
                    # has a chapter, join it in the url
                    page_dest_dir = os.path.join(
                        destination_dir,
                        book_dirname,
                        slugify(this_page['chapter']),
                    )
                else:
                    page_dest_dir = os.path.join(destination_dir, book_dirname)

                os.makedirs(page_dest_dir, exist_ok=True)
                if self.verbose:
                    print(f"Downloading {this_page['url']} to {page_dest_dir}")
                self.export_page( this_page['url'], page_dest_dir)


    def close(self):
        """ close out the http session """

        if self.session:
            self.session.close()

    def __init__(self, bookstack_url, user_email, user_pass, file_type="html", verbose=False):
        """
        Init the class.  Requires the bookstack base url, user email, user password.

        Optional arguments are:
        filetype: html (default), pdf, or plaintext.
        verbose: boolean - enables verbose output
        """

        self.verbose = verbose
        self.url = bookstack_url
        self.user_email = user_email
        self.user_pass = user_pass
        self.file_type = file_type

        self.session = None

        self.books = {}


if __name__ == '__main__':
    # sorry, no functionality here yet.
    pass
