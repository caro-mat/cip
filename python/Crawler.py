import requests
import csv
from bs4 import BeautifulSoup
from bs4 import ResultSet


class Crawler:

    def __init__(self, path):
        self.__path = path
        self.__html = None
        self.__content_table = []

    def __get_path(self):
        return self.__path

    def __set_path(self, path):
        self.__path = path

    def __get_raw_data(self):
        return self.__raw_data

    def __get_html(self):
        return self.__html

    def __get_content_table(self):
        return self.__content_table

    path = property(__get_path, __set_path)
    raw_data = property(__get_raw_data)
    html = property(__get_html)
    content_table = property(__get_content_table)

    def __request_data(self):
        request = RequestProxy(self.__path)
        request.send_request()
        self.__raw_data = request.response

    def crawl(self):
        self.__request_data()
        self.__html = BeautifulSoup(self.raw_data.content, 'html.parser')


class CrawlDataScienceBachelor(Crawler):
    def __init__(self, path):
        super().__init__(path)

    def extract_features(self):
        ###
        # Features sind Dateispezifisch. Deshalb wird das in einer Unterklasse erledigt...
        ###

        eof = False
        items = ResultSet('')
        while not eof:
            # Solange loopen, bis alle Seiten gecrawlt sind
            # List-Items lesen
            page_items = self.html.find_all(class_="program-listitem")
            items += page_items

            # Links lesen
            pagination = self.html.find(class_='pagination')
            links = pagination.find_all('a')
            if not links:
                eof = True
            else:
                # Next-Link ermitteln
                link = links[0]
                button = link.find('button')

                # Prüfen ob "Next"-Link vorliegt. Falls nicht, ist es "Previous". Dann nächsten Link...
                if button.text != 'Next':
                    if len(links) > 1:
                        link = links[1]
                        button = link.find('button')

                        # Püfen ob der 2. Link jetzt Next ist. Falls nicht break...
                        if button.text != 'Next':
                            break
                    else:
                        break
                self.path = link.get('href')
                self.crawl()

        # Gewünschte Features auslesen...
        for item in items:
            try:
                title = item.find('div', class_='title').h4.text
            except Exception as error:
                title = None

            try:
                school = item.find('div', class_='school').text
            except Exception as error:
                school = None

            try:
                location = item.find('span', class_='location').text
                location = location.replace('\n', '').replace(' ', '')
            except Exception as error:
                location = None

            try:
                description = item.find('p', class_='desc').text
                description = description.replace('\n', ' ')
            except Exception as error:
                description = None

            try:
                degree = item.find('div', class_='degree').find('div', class_='label-item').text
                degree = degree.replace('\n', '').replace(' ', '')
            except Exception as error:
                degree = None

            try:
                pace = item.find('div', class_='pace').find('div', class_='label-item').text
            except Exception as error:
                pace = None

            try:
                duration = item.find('div', class_='duration').find('div', class_='label-item').text
            except Exception as error:
                duration = None

            try:
                languages = item.find('div', class_='languages').find('div', class_='label-item').text
                languages = languages.replace('\n', '').replace(' ', '')
            except Exception as error:
                languages = None

            try:
                start = item.find('div', class_='start').find('div', class_='label-item').text
            except Exception as error:
                start = None

            try:
                based = item.find('div', class_='pace').find('div', class_='label-item').text
            except Exception as error:
                based = None

            content_element = [title, school, location, description, degree, pace, duration, languages, start, based]
            self.content_table.append(content_element)


class CrawlDataScienceMaster(Crawler):

    def __init__(self, path):
        super().__init__(path)

    def extract_features(self):
        ###
        # Features sind Dateispezifisch. Deshalb wird das in einer Unterklasse erledigt...
        ###

        eof = False
        items = ResultSet('')
        while not eof:
            # Solange loopen, bis alle Seiten gecrawlt sind
            # List-Items lesen
            page_items = self.html.find_all(class_="program-listitem")
            items += page_items

            # Links lesen
            pagination = self.html.find(class_='pagination')
            links = pagination.find_all('a')
            if not links:
                eof = True
            else:
                # Next-Link ermitteln
                link = links[0]
                button = link.find('button')

                # Prüfen ob "Next"-Link vorliegt. Falls nicht, ist es "Previous". Dann nächsten Link...
                if button.text != 'Next':
                    if len(links) > 1:
                        link = links[1]
                        button = link.find('button')

                        # Püfen ob der 2. Link jetzt Next ist. Falls nicht break...
                        if button.text != 'Next':
                            break
                    else:
                        break
                self.path = link.get('href')
                self.crawl()

        # Gewünschte Features auslesen...
        for item in items:
            try:
                title = item.find('div', class_='title').h4.text
            except Exception as error:
                title = None

            try:
                school = item.find('div', class_='school').text
            except Exception as error:
                school = None

            try:
                location = item.find('span', class_='location').text
                location = location.replace('\n', '').replace(' ', '')
            except Exception as error:
                location = None

            try:
                description = item.find('p', class_='desc').text
                description = description.replace('\n', ' ')
            except Exception as error:
                description = None

            try:
                degree = item.find('div', class_='degree').find('div', class_='label-item').text
                degree = degree.replace('\n', '').replace(' ', '')
            except Exception as error:
                degree = None

            try:
                pace = item.find('div', class_='pace').find('div', class_='label-item').text
            except Exception as error:
                pace = None

            try:
                duration = item.find('div', class_='duration').find('div', class_='label-item').text
            except Exception as error:
                duration = None

            try:
                languages = item.find('div', class_='languages').find('div', class_='label-item').text
                languages = languages.replace('\n', '').replace(' ', '')
            except Exception as error:
                languages = None

            try:
                start = item.find('div', class_='start').find('div', class_='label-item').text
            except Exception as error:
                start = None

            try:
                based = item.find('div', class_='pace').find('div', class_='label-item').text
            except Exception as error:
                based = None

            content_element = [title, school, location, description, degree, pace, duration, languages, start, based]
            self.content_table.append(content_element)


class RequestProxy:

    def __init__(self, path):
        self.__path = path

    def send_request(self):
        self.__response = requests.get(self.__path)
        if self.__response.status_code != 200:
            print("Request failed " + self.__path)
        else:
            print("Request successful " + self.__path)

    def __get_response(self):
        return self.__response

    response = property(__get_response)


class Cleanser:
    pass


class Export:

    def __init__(self, path, file_name):
        self.__path = path
        self.__file_name = file_name

    def export_to_file(self, content):

        full_path = self.__path + self.__file_name
        with open(full_path, 'w', encoding='utf-8', newline='') as file:

            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerows(content)


def main():

    # Master
    crawler1 = CrawlDataScienceMaster('https://www.masterstudies.com/Masters-Degree/Data-Science/')
    crawler1.crawl()
    crawler1.extract_features()
    export1 = Export('', 'test_master.csv')
    export1.export_to_file(crawler1.content_table)

    # Bachelor
    crawler2 = CrawlDataScienceMaster('https://www.bachelorstudies.com/Bachelor/Data-Science/')
    crawler2.crawl()
    crawler2.extract_features()
    export2 = Export('', 'test_bachelor.csv')
    export2.export_to_file(crawler2.content_table)


if __name__ == '__main__':
    main()
