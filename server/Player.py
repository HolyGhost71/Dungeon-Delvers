class Player():

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.gold = 0
        self.items = []
        self.submittedChoice = None

    def add_gold(self, n):
        self.gold += n

    def jsonify(self):
        return {"name": self.name, "gold": self.gold}

    