class TennisGame:
    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_score += 1
        elif player_name == self.player2_name:
            self.player2_score += 1

    def get_score(self):
        if self.is_tie():
            return self.tie_score()
        elif self.is_endgame():
            return self.endgame_score()
        else:
            return self.running_score()

    def is_tie(self):
        return self.player1_score == self.player2_score

    def tie_score(self):
        if self.player1_score < 3:
            return f"{self.SCORE_NAMES[self.player1_score]}-All"
        return "Deuce"

    def is_endgame(self):
        return self.player1_score >= 4 or self.player2_score >= 4

    def endgame_score(self):
        score_difference = self.player1_score - self.player2_score
        if score_difference == 1:
            return f"Advantage {self.player1_name}"
        elif score_difference == -1:
            return f"Advantage {self.player2_name}"
        elif score_difference >= 2:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

    def running_score(self):
        player1_text = self.SCORE_NAMES[self.player1_score]
        player2_text = self.SCORE_NAMES[self.player2_score]
        return f"{player1_text}-{player2_text}"
