from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import csv
import re

# Access the Selenium API
import selenium.common.exceptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class LeagueParser(object):
    """
    A class to parse the Odds Portal website.
    Makes use of Selenium and BeautifulSoup modules
    """

    def __init__(self, starting_url, ex_path=None):
        """
        Constructor providing the executable path value to None
        """
        if ex_path != None:
            self.url = starting_url
            self.browser = webdriver.Chrome(executable_path=ex_path)
            self.browser.get(self.url)
        else:
            self.url = starting_url
            self.browser = webdriver.Chrome()
            self.browser.get(self.url)

    def seasonPages(self):
        """
        Return list of links to seasons pages when on the sport league main webpage.
        """
        html_source = self.browser.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        links_tags = soup.find(
            "div", class_="main-menu2 main-menu-gray").find_all("span")
        links_webpages = ["http://www.oddsportal.com/" +
                          tag.find("a")['href'] + "#" for tag in links_tags]
        return links_webpages

    def pagination(self, soup, error=None):
        """
        Returns the page's pagination for the first page of a single
        season on the Odds Portal website.
        """
        pages_ = []
        try:
            pagination_tags = soup.find("div", id="pagination")
            list_ = [page['href'] for page in pagination_tags.find_all("a")]
            pages_ = []
            for page in list_:
                if re.search('\d', str(page)) is None:
                    pass
                else:
                    if page not in pages_:
                        pages_.append(page)
            return pages_
        except AttributeError as NoPages:
            if error is not None:
                print NoPages, "No pagination found for the season."
            return None

    def cellsData(self, table):
        """
        Returns the urls to the match's details and each cell's data
        """
        main_url = "http://www.oddsportal.com/"
        match_hour, teams, score, odd_home = [], [], [], []
        odd_draw, odd_away, odd_tot, urls = [], [], [], []
        for tr in table.find_all("tr"):
            for num, td in enumerate(tr.find_all("td")):
                if num == 0 and td.get_text() != u'':
                    match_hour.append(td.get_text())  # Match hours
                elif num == 1 and td.get_text() != u'':
                    teams.append(td.get_text())  # Teams or Players
                    urls.append(td.a['href'])  # Links to the match details
                elif num == 2 and td.get_text() != u'':
                    score.append(td.get_text())  # Score
                elif num == 3 and td.get_text() != u'':
                    odd_home.append(td.get_text())  # Average odd for team 1
                elif num == 4 and td.get_text() != u'':
                    odd_draw.append(td.get_text())  # Average odd for draw
                elif num == 5 and td.get_text() != u'':
                    odd_away.append(td.get_text())  # Average odd for team 2
                elif num == 6 and td.get_text() != u'':
                    odd_tot.append(td.get_text())  # Number of bookies

        urls = [main_url + url for url in urls]
        return [urls, match_hour, teams, score, odd_home, odd_draw, odd_away, odd_tot]

    def highestOdds(self, soup):
        highest_home, highest_draw, highest_away = "", "", ""
        row_to_parse = soup.find("tr", class_="highest")
        for num, td in enumerate(row_to_parse.find_all("td", class_="right")):
            if num == 0:
                highest_home = highest_home + td.get_text()
            elif num == 1:
                highest_draw = highest_draw + td.get_text()
            elif num == 2:
                highest_away = highest_away + td.get_text()
        return highest_home, highest_draw, highest_away

    def archivedResults(self, page_source):
        """
        This function parses the "Archived Results Page".
        It returns a list of dict, with the tournament name as the key and the
        url to the tournament as a value.
        """
        sports_leagues_dict = []
        page_soup = BeautifulSoup(page_source, 'html.parser')
        active_rows = page_soup.find_all('tr', style='display: table-row;')

        # Selecting only the active rows
        # Now deleting the head rows
        no_head_rows = [row for row in active_rows if row.find("th") == None]

        # Checks the links within rows composed of a single cell are in the list
        # 2 lists for the rows with a single cell (TypeError returned in that case.)
        excepted_rows, links_tournaments = [], []
        for row in no_head_rows:
            for td in row.find_all("td"):
                try:
                    links_tournaments.append(td.a["href"])
                    sports_leagues_dict.append(
                        dict([
                            ("Tournament Name", td.get_text().encode('utf-8')),
                            ("url", "http://www.oddsportal.com" + td.a["href"].encode('utf-8'))
                        ])
                    )

                except TypeError:
                    excepted_rows.append(row)
                    print "Row with single cell: ", row.get_text()

        for row in excepted_rows:
            sports_leagues_dict.append(
                dict([
                    ("Tournament Name", row.get_text().encode('utf-8')),
                    ("url", 'http://www.oddsportal.com' + row.find("td").a["href"].encode('utf-8'))
                ])
            )

        # Do a list of tuples with each dict in the tennis_dict list. Then, use set() to remove
        # duplicates and finally reconvert each tuple to a dict.
        sports_leagues_dict = [dict(t) for t in set([tuple(d.items())
                                                     for d in sports_leagues_dict])]
        return sports_leagues_dict
        # Map a dict whose key is the name of the tournament and the value is the link to it.
