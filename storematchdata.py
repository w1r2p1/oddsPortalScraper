import sys
sys.path.append(
    '/Users/dmpierre/Documents/PyScripts/MyScripts/my_modules/oddscraper'
)

import matchdetails


def cancelledMatch(part_match_dict, soup):
    """
    Takes as argument a part_match_dict and a parsed soup page
    """
    match_details = matchdetails.matchData(soup, cancel=True)
    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Set cancelled game to 1
    part_match_dict['cancelled_game'] = 1

    return part_match_dict


def retiredPlayer(part_match_dict, soup):
    """
    Takes as argument a part_match_dict and a parsed soup page
    Case for retired player.
    """
    # Set the match detail function retired value to True
    match_details = matchdetails.matchData(soup, retired=True)

    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Set retired player to 1
    part_match_dict['retired_player'] = 1

    return part_match_dict


def walkoverPlayer(part_match_dict, soup):
    """
    Case for a player who walked over.
    """
    match_details = matchdetails.matchData(soup, walkover=True)
    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Set retired player to 1
    part_match_dict['walkover'] = 1

    return part_match_dict


def awardedPlayer(part_match_dict, soup):

    match_details = matchdetails.matchData(soup, awarded=True)
    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Collect final result
    part_match_dict['player_1_score'], part_match_dict['player_2_score'] = match_details[2][0].split(
        ':')
    part_match_dict['player_1_score'] = int(part_match_dict['player_1_score'])
    part_match_dict['player_2_score'] = int(part_match_dict['player_2_score'])

    # Set awarded to one
    part_match_dict['awarded_player'] = 1

    return part_match_dict


def noSetInfo(part_match_dict, soup):
    """
    Takes as argument a part_match_dict and a parsed soup page
    """
    match_details = matchdetails.matchData(soup, no_set_info=True)

    # First, the match date, hour and players name.
    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Get the final result
    part_match_dict['player_1_score'] = int(
        match_details[2][0]) if match_details[2][0] != '' else ''
    part_match_dict['player_2_score'] = int(
        match_details[2][1]) if match_details[2][0] != '' else ''

    part_match_dict['no_set_info'] = 1
    return part_match_dict


def normalMatch(part_match_dict, soup):
    """
    Takes as argument a part_match_dict and a parsed soup page
    """
    match_details = matchdetails.matchData(soup)

    # First, the match date, hour and players name.
    part_match_dict['day'], part_match_dict['date'] = match_details[1][0], match_details[1][1]
    part_match_dict['hour'] = float(match_details[1][2].replace(':', '.'))
    part_match_dict['player_1_name'], part_match_dict['player_2_name'] = match_details[0][0], match_details[0][1]

    # Get the final result
    part_match_dict['player_1_score'] = int(
        match_details[2][0]) if match_details[2][0] != '' else ''
    part_match_dict['player_2_score'] = int(
        match_details[2][1]) if match_details[2][0] != '' else ''

    # Now, each set details, not keeping special set scores.
    for num, single_set in enumerate(match_details[3]):

        player_1_set, player_2_set = single_set.split(':')
        part_match_dict['player_1_set_' + str(num)] = int(player_1_set.replace(' ', '')[0])
        part_match_dict['player_2_set_' + str(num)] = int(player_2_set.replace(' ', '')[0])

    return part_match_dict
