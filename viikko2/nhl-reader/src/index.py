from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table
from rich.style import Style
def main():
    console = Console()

    season = input("Select season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25]: ")

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    while True:
    	nationality = input("Select nationality [AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR or STOP]: ")
    	if nationality == "STOP":
      		break
    	players = stats.top_scorers_by_nationality(nationality)

    	table = Table(show_header=True, header_style="bold white")
    	table.add_column("name", style="blue", width=20)
    	table.add_column("team", style="magenta", width=8)
    	table.add_column("goals", style="green",justify="right")
    	table.add_column("assists", style="green", justify="right")
    	table.add_column("points", style="green", justify="right")
    

    	for player in players:
        	table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points))

    	console.print(table)

if __name__ == "__main__":
    main()
