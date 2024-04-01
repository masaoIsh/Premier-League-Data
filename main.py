import requests
from bs4 import BeautifulSoup
import csv


def convert_to_last_names(array):
    last_names = []
    for player in array:
        try:
            last_name = player.split()[1]
        except IndexError:
            last_name = player.split()[0]
        last_names.append(last_name)
    return last_names


base_url = "https://www.premierleague.com/stats"
response = requests.get(base_url)

# Convert to beautifulsoup object
soup = BeautifulSoup(response.content, "html.parser")

# Print webpage html
# print(soup.prettify())

listed_players_and_teams = soup.find_all(class_="top-stats__row-name")
listed_players = [element for element in listed_players_and_teams if "/players/" in element['href']]

# Full names of players
goal_scorers_full = [element.text for element in listed_players[:9]]
assist_players_full = [element.text for element in listed_players[9:18]]
pass_players_full = [element.text for element in listed_players[18:27]]
clean_sheets_full = [element.text for element in listed_players[27:36]]

# Last names only
goal_scorers = convert_to_last_names(goal_scorers_full)
assist_players = convert_to_last_names(assist_players_full)
pass_players = convert_to_last_names(pass_players_full)
clean_sheets = convert_to_last_names(clean_sheets_full)

# Players in first place
top_players_lm_elements = soup.find_all(class_="top-stats__hero-last")
top_players = [element.text.strip() for element in top_players_lm_elements]

# Numbers of non-first place players
stat_elements = soup.find_all(class_="top-stats__row-stat")
stats = [element.text.strip() for element in stat_elements[:36]]

# Create array of tuples with stats
goal_ranking = []
assist_ranking = []
pass_ranking = []
clean_sheet_ranking = []
for i in range(len(goal_scorers)):
    goal_tuple = (goal_scorers[i], int(stats[i]))
    assist_tuple = (assist_players[i], int(stats[i + 9]))
    pass_tuple = (pass_players[i], int(stats[i + 18].replace(',', '')))
    clean_sheet_tuple = (clean_sheets[i], int(stats[i + 27]))
    goal_ranking.append(goal_tuple)
    assist_ranking.append(assist_tuple)
    pass_ranking.append(pass_tuple)
    clean_sheet_ranking.append(clean_sheet_tuple)


# Write to CSV
file_name = "PremierLeagueData.csv"
zipped_list = list(zip(goal_ranking, assist_ranking, pass_ranking, clean_sheet_ranking))

with open(file_name, 'w', encoding="utf-8") as f:
    f.write = csv.writer(f)
    f.write.writerow(['Goals', 'Assists', 'Passes', 'Clean Sheets'])

    for row in zipped_list:
        f.write.writerow(row)

