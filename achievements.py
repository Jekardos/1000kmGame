ACHIEVEMENTS = {
    "Путешественник": {
        "description": "Достичь 100-й клетки",
        "reward": 500,
        "completed": False,
        "check": lambda stats: stats["player_position"] >= 100
    },
    "Богач": {
        "description": "Накопить 1000 JK",
        "reward": 1000,
        "completed": False,
        "check": lambda stats: stats["money"] >= 1000
    },
    "Игрок": {
        "description": "Выиграть 10 игр",
        "reward": 300,
        "completed": False,
        "check": lambda stats: stats["games_won"] >= 10
    },
    "Ветеран": {
        "description": "Сделать 50 ходов",
        "reward": 200,
        "completed": False,
        "check": lambda stats: stats["turn_count"] >= 50
    },
    "Заботливый хозяин": {
        "description": "Поддерживать здоровье собаки выше 80% на протяжении 10 ходов",
        "reward": 400,
        "completed": False,
        "check": lambda stats: stats["dog_health"] >= 80
    },
    "Монетизатор": {
        "description": "Получить 500 JK от монетизации",
        "reward": 800,
        "completed": False,
        "check": lambda stats: stats.get("monetization_earnings", 0) >= 500
    },
    "Популярный блогер": {
        "description": "Получить 10 донатов от подписчиков",
        "reward": 600,
        "completed": False,
        "check": lambda stats: stats.get("donations_received", 0) >= 10
    },
    "Спонсор": {
        "description": "Заключить 5 спонсорских контрактов",
        "reward": 1000,
        "completed": False,
        "check": lambda stats: stats.get("sponsor_deals", 0) >= 5
    }
} 