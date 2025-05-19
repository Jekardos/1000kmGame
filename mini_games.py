import random

MINI_GAMES = {
    "Стрим": {
        "description": "Проведите стрим о своем путешествии",
        "energy_cost": 15,
        "donation_chance": 0.7,
        "donation_range": (20, 100)
    },
    "Мерч": {
        "description": "Продайте мерч с логотипом вашего путешествия",
        "energy_cost": 25,
        "sales_chance": 0.6,
        "sales_range": (30, 150)
    }
}

def play_mini_game(game_data, bet=None):
    if "donation_chance" in game_data:
        if random.random() < game_data["donation_chance"]:
            donation = random.randint(game_data["donation_range"][0], game_data["donation_range"][1])
            return True, donation
    elif "sales_chance" in game_data:
        if random.random() < game_data["sales_chance"]:
            sales = random.randint(game_data["sales_range"][0], game_data["sales_range"][1])
            return True, sales
    return False, 0 