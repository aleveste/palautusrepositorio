import requests

class Player:
    def __init__(self, player_data):
        self.name = player_data.get("name", "N/A")
        self.team = player_data.get("team", "N/A")
        self.nationality = player_data.get("nationality", "N/A")
        self.goals = player_data.get("goals", 0)
        self.assists = player_data.get("assists", 0)
        self.points = self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} {self.team}  {self.goals} + {self.assists} = {self.points}"

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()
        players = [Player(player_dict) for player_dict in response]
        return players

class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        filtered_players = list(filter(lambda p: p.nationality == nationality, self.players))
        sorted_players = sorted(filtered_players, key=lambda p: p.points, reverse=True)
        return sorted_players
