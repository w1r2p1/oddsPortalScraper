from bs4 import BeautifulSoup
import sys
# Appending the python path to the module folder.
sys.path.append(r"C:\Python27\Scripts\Myscripts\MY_MODULES\OddsScrapingModules")


"""
Try to remain simple for the moment. For instance just use
a function if you want to retrieve the highest odd available.
Everything is then about Data Analysis. Just scrape the essential.
"""


def bookieData(soup_table, bookie):
    """
    The soup table arugument is a beautiful soup parsed table of the match.
    The bookie argument is the name of a bookie I want to parse the odds.
    """
    home, away, payout = '', '', ''
    row = soup_table.find(href="/bookmaker/" + bookie + "/link/").parent.parent.parent

    for num, cell in enumerate(row.find_all('td')):
        if num is 1:
            home = float(home + cell.get_text()) if cell.get_text() not in (u'-' or '') else ''
        if num is 2:
            away = float(away + cell.get_text()) if cell.get_text() not in (u'-' or '') else ''
        if num is 3:
            payout = float(payout + cell.get_text().replace('%', '')
                           ) if cell.get_text() not in (u'-' or '') else ''
        else:
            pass

    return [home, away, payout]


def matchData(soup, cancel=None, retired=None, awarded=None, walkover=None, no_set_info=None):
    """
    For tennis only up to now.
    """
    content = soup.find('div', id='col-content')

    # Get rid of the span tag.
    span = content.span.extract()

    # Basic match info.
    players = content.h1.get_text().split(' - ')
    date_time = content.p.get_text().split(', ')

    if cancel or walkover or retired is not None:
        # When the match got cancelled
        return [players, date_time]

    else:

        all_result = content.find('p', class_='result').get_text()

        # When only the final result is here.
        if no_set_info is not None:
            final_result = content.find('p', class_='result').strong.get_text()
            final_result = final_result.split(':') if final_result != u'' else ['']
            return [players, date_time, final_result]

        set_info = all_result.split('(')[1].replace(')', '')
        single_sets = [result for result in set_info.split(',')]

        if awarded is not None:
            # Single sets is the final score here!!
            return [players, date_time, single_sets]

        else:
            # Getting the final result
            final_result = content.find('p', class_='result').strong.get_text()
            final_result = final_result.split(':') if final_result != u'' else ['']

            return [players, date_time, final_result, single_sets]


def detectBookieData(soup):
    """
    Returns whether there is actually bookies odds data.
    """
    return soup.find('div', class_='table-container')


def detectCancelled(soup):
    """
    Return whether the match has been cancelled or not.
    Returns True in case it has been cancelled, False otherwise.
    """
    content = soup.find('div', id='col-content')
    if content.find('p', class_='result-alert') is not None:
        return True
    else:
        return None


def detectRetired(soup):
    """
    Detect whether one of the players retired or not.
    """
    content = soup.find('div', id='col-content')
    final_result = content.find('p', class_='result').strong.get_text()

    if final_result.find('retired') is -1:
        # If .find() returns -1, then it didn't find 'retired'
        return None
    else:
        return True


def detectWalkover(soup):
    """
    Detect whether the player walked over.
    """
    content = soup.find('div', id='col-content')
    final_result = content.find('p', class_='result').strong.get_text()
    if final_result.find('walkover') is -1:
        return None
    else:
        return True


def detectAwarded(soup):
    """
    Detect whether one of the two players got awarded.
    """
    content = soup.find('div', id='col-content')
    final_result = content.find('p', class_='result').strong.get_text()

    if final_result.find('awarded') is -1:
        return None
    else:
        return True


def noSetInfo(soup):
    """
    Detect whether there is information about the single sets.
    """
    content = soup.find('div', id='col-content')
    all_result = content.find('p', class_='result').get_text()
    if all_result.find('(') is -1:
        return True
    else:
        return None


def createMatchDict(bookies_name_list):
    """
    Returns a ready to use dict for storing match bookie and general data
    """
    part_match_dict = {
        u'url': '', u'tournament_name': '',
        u'country': '',
        u'day': '', u'date': '', u'hour': '',
        u'player_1_name': '', u'player_2_name': '',
        u'player_1_score': '', u'player_2_score': '',
        u'retired_player': 0, u'cancelled_game': 0,
        u'awarded_player': 0,
        u'error': 0, u'comments': '', u'missing_bookies': 0,
        u'walkover': 0, u'no_set_info': 0
    }

    for i in range(5):
        part_match_dict[u'player_1_set_' + str(i)] = ''
        part_match_dict[u'player_2_set_' + str(i)] = ''

    for name in bookies_name_list:
        part_match_dict[name + '_player_1_odd'] = ''
        part_match_dict[name + '_player_2_odd'] = ''
        part_match_dict[name + '_payout'] = ''

    return part_match_dict
