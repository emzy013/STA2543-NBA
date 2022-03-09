from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def get_player_stats(year=2020, playoffs=False):
    """
    Get on-court performance stats per NBA player.
    """

    # Get corresponding url at basketball-reference.com.
    if playoffs:
        keyword = "playoffs"
    else:
        keyword = "leagues"
    url = "https://www.basketball-reference.com/{}/NBA_{}_per_game.html".format(keyword, year)

    # Download data.
    soup = BeautifulSoup(urlopen(url), features="html.parser")

    # Table has this format:
    # th th th
    # th td td
    # th td td

    # Get the headers.
    column_names = soup.findAll('thead')[0] \
        .findAll('tr')[0] \
        .findAll('th')
    headers = []
    for column_name in column_names:
        headers.append(column_name.getText())
    # Remove column name for index
    headers = headers[1:]

    # Get the actual stats.
    rows = soup.findAll('tbody')[0] \
        .findAll('tr')
    player_stats = []
    for row in rows:
        player_stat = [td.getText() for td in row.findAll('td')]
        player_stats.append(player_stat)

    # Import to dataframe
    df = pd.DataFrame(player_stats, columns=headers)

    # Drop all additional headers (none in data)
    df.dropna(inplace=True)

    return df


def get_team_stats(year=2020, playoffs=False):
    """
    Get on-court performance stats per NBA team.
    """

    # Get corresponding url at basketball-reference.com.
    if playoffs:
        keyword = "playoffs"
    else:
        keyword = "leagues"
    url = "https://www.basketball-reference.com/{}/NBA_{}.html".format(keyword, year)

    # Download data.
    soup = BeautifulSoup(urlopen(url), features="html.parser")

    # Get the headers.
    column_names = soup.findAll('table', id='per_game-team')[0] \
        .findAll('thead')[0] \
        .findAll('tr')[0] \
        .findAll('th')
    headers = []
    for column_name in column_names:
        headers.append(column_name.getText())
    # Remove column name for index
    headers = headers[1:]

    # Get the actual stats.
    rows = soup.findAll('table', id='per_game-team')[0] \
        .findAll('tbody')[0] \
        .findAll('tr')
    player_stats = []
    for row in rows:
        player_stat = [td.getText() for td in row.findAll('td')]
        player_stats.append(player_stat)

    # Import to dataframe
    df = pd.DataFrame(player_stats, columns=headers)

    # Drop all additional headers (none in data)
    df.dropna(inplace=True)

    return df


def get_player_salaries(year=2020):
    """
    Get salaries per player.
    """

    # Get corresponding url at hoopshype.com.
    if year == 2021:
        # No specifier needed for current season.
        season = ''
    else:
        season = str(year) + '-' + str(year + 1)
    url = "https://hoopshype.com/salaries/players/{}".format(season)

    # Download data.
    soup = BeautifulSoup(urlopen(url), features="html.parser")

    # Get the headers.
    headers = ['Player', 'Salary', 'Adjusted']

    # Get the actual data.
    rows = soup.findAll('table')[0] \
        .findAll('tbody')[0] \
        .findAll('tr')
    player_salaries = []
    for row in rows:
        player_salary = [td.getText(strip=True) for td in row.findAll('td')]
        if year == 2021:
            # For current season, salary is the same as the adjusted value.
            row_val = player_salary[1:3] + [player_salary[2]]
        else:
            row_val = player_salary[1:4]
        player_salaries.append(row_val)

    # Import to dataframe
    df = pd.DataFrame(player_salaries, columns=headers)

    # Drop all additional headers (none in data)
    df.dropna(inplace=True)

    return df


def get_team_salaries(year=2020):
    """
    Get total salaries paid per team.
    """

    # Get corresponding url at hoopshype.com.
    if year == 2021:
        # No specifier needed for current season.
        season = ''
    else:
        season = str(year) + '-' + str(year + 1)
    url = "https://hoopshype.com/salaries/{}".format(season)

    # Download data.
    soup = BeautifulSoup(urlopen(url), features="html.parser")

    # Get the headers.
    headers = ['Team', 'Salary', 'Adjusted']

    # Get the actual data.
    rows = soup.findAll('table')[0] \
        .findAll('tbody')[0] \
        .findAll('tr')
    team_salaries = []
    for row in rows:
        team_salary = [td.getText(strip=True) for td in row.findAll('td')]
        if year == 2021:
            # For current season, salary is the same as the adjusted value.
            row_val = team_salary[1:3] + [team_salary[2]]
        else:
            row_val = team_salary[1:4]
        team_salaries.append(row_val)

    # Import to dataframe
    df = pd.DataFrame(team_salaries, columns=headers)

    # Drop all additional headers (none in data)
    df.dropna(inplace=True)

    return df


def get_salary_caps():
    """
    Get salary cap per season, from 1984-85 to 2021-22.
    """

    url = "https://www.spotrac.com/nba/cba/"

    # Download data.
    soup = BeautifulSoup(urlopen(url), features="html.parser")

    # Get the headers.
    headers = ['Year', "Salary Cap"]

    # Get the actual data.
    rows = soup.findAll('table')[0] \
        .findAll('tbody')[0] \
        .findAll('tr')
    salary_caps = []
    for row in rows:
        caps = [td.getText(strip=True) for td in row.findAll('td')]
        caps = caps[:2]
        salary_caps.append(caps)

    # Import to dataframe
    df = pd.DataFrame(salary_caps, columns=headers)

    # Drop all additional headers (none in data)
    df.dropna(inplace=True)

    return df


if __name__ == "__main__":
    years = [i for i in range(2000, 2022)]

    # Get salary caps data.
    get_salary_caps().to_csv('../data/raw/salary_caps.csv', index=False)

    for year in years:
        get_player_stats(year=year).to_csv('../data/raw/player_stats_' + str(year) + '.csv', index=False)
        get_team_stats(year=year).to_csv('../data/raw/team_stats_' + str(year) + '.csv', index=False)
        get_player_salaries(year=year).to_csv('../data/raw/player_salaries_' + str(year) + '.csv', index=False)
        get_team_salaries(year=year).to_csv('../data/raw/team_salaries_' + str(year) + '.csv', index=False)
