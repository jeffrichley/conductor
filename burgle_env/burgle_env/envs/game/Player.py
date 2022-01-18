

class Player():

    def __init__(self, player_num):

        self.player_num = player_num
        self.location = (-1, -1, -1)
        self.num_stealth_tokens = 3


    def move_to(self, location):

        self.location = location