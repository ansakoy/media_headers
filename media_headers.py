import datetime
import requests

from header_surfer import HeadersSurfer


OTHER_MEDIA = ["the-washington-post", "the-telegraph", "the-new-york-times",
               "the-huffington-post", "the-guardian-uk", "reuters", "newsweek",
               "cnn", "cnbc", "business-insider", "breitbart-news", "bbc-news",
               "al-jazeera-english"]


def load_key(key=None):
    try:
        with open('newsapi_key.txt', 'r') as my_key:
            return my_key.read()
    except FileNotFoundError:
        if key:
            with open('newsapi_key.txt', 'wb') as fhandler:
                fhandler.write(key)
            with open('newsapi_key.txt', 'r') as my_key:
                return my_key.read()
        else:
            print("GIVE ME NORMAL NEWSAPI KEY!")
            return

class TheEconomist(HeadersSurfer):

    def __init__(self, handler=None):
        HeadersSurfer.__init__(self, handler)
        self.url = 'https://www.economist.com/'
        self.name = 'The Economist'
        self.limits = (300000, 450000)
        self.article_url = ''
        self.api_mode = False
        try:
            page_content = self.get_page(self.url, limits=self.limits)
            headers_area = str(self.get_area(page_content, 'div', class_='hero-component'))
            self.teaser_headers = self.get_header_blocks(headers_area, 'a', class_='teaser__link')
            self.recent_headers = self.get_header_blocks(headers_area, 'a', class_='latest-updates-panel-card')
        except IndexError:
            self.api_mode = True
            alert = 'SWITCHED TO NEWS API FOR THE ECONOMIST'
            # print(alert)
            if self.handler:
                self.write_to_txt(alert + '\n')
        # print(self.name, self.url)
        if self.handler:
            self.write_to_txt(self.name + '\n')
            self.write_to_txt(self.url + '\n')
        print(str(datetime.datetime.now()))

    def process_headers(self):
        if self.api_mode:
            key = load_key()
            url = 'https://newsapi.org/v1/articles?source=the-economist&sortBy=top&apiKey=' + key
            response = requests.get(url).json()
            articles = response['articles']
            for article in articles:
                article_url = (article.get('url', 'No url') + '\n')
                title = (article.get('title', 'No title') + '\n')
                try:
                    description = (article.get('description', 'No description') + '\n\n')
                except TypeError:
                    description = 'No description\n\n'
                if self.handler:
                    self.write_to_txt(article_url)
                    self.write_to_txt(title)
                    self.write_to_txt(description)

        else:
            for header in self.teaser_headers:
                href = header.get('href')
                header_area = str(header)
                flytitle = self.get_text(header_area, 'span', class_='flytitle-and-title__flytitle')
                title = self.get_text(header_area, 'span', class_='flytitle-and-title__title')
                lead = self.get_lead(href)
                # print('\n', self.article_url)
                title = flytitle + ': ' + title
                # print(title)
                # print(lead)
                if self.handler:
                    self.write_to_txt(self.article_url + '\n')
                    try:
                        self.write_to_txt(title + '\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write title\n')
                    try:
                        self.write_to_txt(lead + '\n\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write lead\n\n')
            for header in self.recent_headers:
                href = header.get('href')
                header_area = str(header)
                title = self.get_text(header_area, 'h3', class_='latest-updates-panel-card__title')
                lead = self.get_lead(href)
                # print('\n', self.article_url)
                # print(title)
                # print(lead)
                if self.handler:
                    self.write_to_txt(self.article_url + '\n')
                    try:
                        self.write_to_txt(title + '\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write title\n')
                    try:
                        self.write_to_txt(lead + '\n\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write lead\n\n')

    def get_lead(self, href):
        self.article_url = self.url + href
        article_page = self.get_page(self.article_url, limits=self.limits)
        try:
            lead = self.get_text(article_page, 'p', class_='blog-post__rubric')
        except Exception as e:
            print('Error:', e)
            print(self.article_url)
            lead = 'none'
        return lead


class WallStreetJournal(HeadersSurfer):

    def __init__(self, handler=None):
        HeadersSurfer.__init__(self, handler)
        self.url = u'https://www.wsj.com/europe'
        self.name = u'Wall Street Journal (Europe)'
        page_content = self.get_page(self.url)
        headers_area = str(self.get_area(page_content, 'div', class_='lead-story'))
        self.headers = self.get_header_blocks(headers_area, 'div', class_='wsj-card')
        # print(str(datetime.datetime.now()))
        # print(self.name, self.url)
        if self.handler:
            self.write_to_txt(self.name + '\n')
            self.write_to_txt(self.url + '\n')

    def process_headers(self):
        for header in self.headers:
            header_area = str(header)
            article_url = self.get_href(header_area, 'a', class_='wsj-headline-link')
            title = self.get_text(header_area, 'a', class_='wsj-headline-link')
            try:
                lead_area = self.get_area(header_area, 'p', class_='wsj-summary')
                lead = lead_area.find('span').text
                # print('\n', article_url)
                # print(title)
                # print(lead)
                if self.handler:
                    self.write_to_txt(article_url + '\n')
                    try:
                        self.write_to_txt(title + '\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write title\n')
                    try:
                        self.write_to_txt(lead + '\n\n')
                    except UnicodeDecodeError:
                        self.write_to_txt('Failed to write lead\n\n')
                    # self.write_to_txt(title + '\n')
                    # self.write_to_txt(lead + '\n\n')
            except IndexError:
                pass


class Bloomberg(HeadersSurfer):

    def __init__(self, handler=None):
        HeadersSurfer.__init__(self, handler)
        self.url = 'https://www.bloomberg.com/europe'
        self.name = 'Bloomberg (Europe)'
        self.article_url = ''
        page_content = self.get_page(self.url)
        top_headers_area = str(self.get_area(page_content, 'div', class_='hero-v6__stories'))
        editorials_area = str(self.get_area(page_content, 'div', class_='home__highlights'))
        self.top_headers = self.get_header_blocks(top_headers_area, 'div', class_='hero-v6-story')
        self.editorials = self.get_header_blocks(editorials_area, 'a', class_='commentary-v6-story__headline-link')
        # print(str(datetime.datetime.now()))
        # print(self.name, self.url)
        if self.handler:
            self.write_to_txt(self.name + '\n')
            self.write_to_txt(self.url + '\n')

    def process_headers(self):
        for header in self.top_headers:
            try:
                title_area = self.get_area(str(header), 'a', class_='hero-v6-story__headline-link')
                title = title_area.text
                url_area = self.get_area(str(header), 'a', class_='hero-v6-story__image')
                href = url_area.get('href')
                try:
                    lead = self.get_lead(href)
                    # print('\n', self.article_url)
                    # print(title)
                    # print(lead)
                    if self.handler:
                        self.write_to_txt(self.article_url + '\n')
                        # self.write_to_txt(title + '\n')
                        # self.write_to_txt(lead + '\n\n')
                        try:
                            self.write_to_txt(title + u'\n')
                        except UnicodeDecodeError:
                            self.write_to_txt(u'Failed to write title\n')
                        try:
                            self.write_to_txt(lead + u'\n\n')
                        except UnicodeDecodeError:
                            self.write_to_txt(u'Failed to write lead\n\n')
                except Exception as e:
                    print('Error:', e)
                    print(self.article_url)
            except IndexError:
                pass
        for header in self.editorials:
            href = header.get('href')
            title = header.text
            lead = self.get_lead(href)
            # print('\n', self.article_url)
            # print(title)
            # print(lead)
            if self.handler:
                self.write_to_txt(self.article_url + '\n')
                # self.write_to_txt(title + '\n')
                # self.write_to_txt(lead + '\n\n')
                try:
                    self.write_to_txt(title + '\n')
                except UnicodeDecodeError:
                    self.write_to_txt(u'Failed to write title\n')
                try:
                    self.write_to_txt(lead + '\n\n')
                except UnicodeDecodeError:
                    self.write_to_txt(u'Failed to write lead\n\n')

    def get_lead(self, href):
        self.article_url = href
        article_page = self.get_page(self.article_url)
        article_area = self.get_area(article_page, 'div', class_='body-copy')
        paragraphs = article_area.find_all('p')
        if paragraphs[0].find('em'):
            lead = paragraphs[1].text
        else:
            lead = paragraphs[0].text
        return lead


class Others(HeadersSurfer):

    def __init__(self, handler=None):
        HeadersSurfer.__init__(self, handler)
        self.key = load_key()
        self.url_base = 'https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey=' + self.key

    def walk_through(self):
        for entry in OTHER_MEDIA:
            # print(entry)
            api_url = self.url_base.format(entry)
            # print api_url
            self.collect_data(api_url)
        # print('DONE')

    def collect_data(self, url):
        response = requests.get(url).json()
        source = (response['source'] + u'\n')
        if self.handler:
            self.write_to_txt(source)
        articles = response['articles']
        for article in articles:
            url = (article.get('url', u'No url') + u'\n')
            title = (article.get('title', u'No title') + u'\n')
            try:
                description = (article.get('description', u'No description') + u'\n\n')
            except TypeError:
                description = u'No description\n\n'
            if self.handler:
                self.write_to_txt(url)
                self.write_to_txt(title)
                self.write_to_txt(description)


if __name__ == '__main__':
    economist = TheEconomist()
    economist.process_headers()
    bloomberg = Bloomberg()
    bloomberg.process_headers()
    wsj = WallStreetJournal()
    wsj.process_headers()
    others = Others()
    others.walk_through()


