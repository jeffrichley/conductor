

class BasicScoringObserver():

    def __init__(self, game):
        self.game = game
        self.vault_was_opened = None
        self.previous_cracked_number = None

    def before_action(self):
        self.vault_was_opened = self.game.vault_opened
        # we need to subtract 1 because it is 1 based and will never have 0 be False
        self.previous_cracked_number = self.game.vault_combination_cracked.count(True) - 1

    def after_action(self):

        done = False

        # we need to subtract 1 because it is 1 based and will never have 0 be False
        current_cracked_number = self.game.vault_combination_cracked.count(True) - 1

        # Rewards
        # 100 for winning
        # -100 for losing
        # 10 for cracking the safe
        # 1 for cracking a number of the safe
        # -1 for any other actions
        all_players_left = True
        for player in self.game.players:
            if player.location[0] == 0:
                all_players_left = False

        reward = -1
        if self.game.players_won():
            reward = 100
            done = True
        elif all_players_left:
            reward = -100
            done = True
        elif self.game.vault_opened and not self.vault_was_opened:
            reward = 10
        elif current_cracked_number > self.previous_cracked_number:
            reward = 1

        return reward, done