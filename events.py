import random

EVENTS = {
    # Положительные события (50)
    "cobra_throw": {
        "name": "Бросок Кобры",
        "description": "Вы чувствуете небывалый прилив сил и решаете пройти в два раза больше обычного!",
        "effect": "special_move",
        "value": 8,
        "energy_cost": 35,
        "type": "positive"
    },
    "anaconda_rush": {
        "name": "Рывок Анаконды",
        "description": "Вы решили сделать мощный рывок! Это позволит пройти в 3 раза дальше обычного, но потребует много сил и здоровья.",
        "effect": "special_move",
        "value": 12,
        "energy_cost": 50,
        "health_cost": 20,
        "skip_turn": True,
        "type": "positive"
    },
    "dog_heal": {
        "name": "Встреча с ветеринаром",
        "description": "В деревне вы встретили ветеринара, который помог вашей собаке.",
        "effect": "dog_health",
        "value": 25,
        "type": "positive"
    },
    "energy_boost": {
        "name": "Находка энергетика",
        "description": "Вы нашли энергетический напиток!",
        "effect": "energy",
        "value": 30,
        "type": "positive"
    },
    "food_cache": {
        "name": "Тайник с провизией",
        "description": "Вы нашли спрятанный тайник с едой и водой. Похоже, его оставили другие путешественники.",
        "effect": "energy",
        "value": 35,
        "type": "positive"
    },
    "kind_villagers": {
        "name": "Добрые жители",
        "description": "Местные жители поделились с вами едой и дали отдохнуть в тени.",
        "effect": "energy",
        "value": 30,
        "type": "positive"
    },
    "shortcut": {
        "name": "Тропа местных",
        "description": "Вы нашли тропу, которая сокращает путь. Местные жители часто ею пользуются.",
        "effect": "special_move",
        "value": 3,
        "energy_cost": 25,
        "type": "positive"
    },
    "medicine_find": {
        "name": "Аптечка",
        "description": "Вы нашли брошенную аптечку с лекарствами. К счастью, они еще годны.",
        "effect": "player_health",
        "value": 25,
        "type": "positive"
    },
    "dog_training": {
        "name": "Тренировка собаки",
        "description": "Ваша собака стала выносливее после тренировки!",
        "effect": "dog_health",
        "value": 20,
        "type": "positive"
    },
    "good_weather": {
        "name": "Хорошая погода",
        "description": "Отличная погода для путешествия!",
        "effect": "energy",
        "value": 15
    },
    "fresh_forces": {
        "name": "С новыми силами",
        "description": "После хорошего отдыха в городе вы чувствуете прилив сил!",
        "effect": "bonus_move",
        "value": 1,
        "type": "positive"
    },
    "survival_skills": {
        "name": "Навыки выживания",
        "description": "Вы используете свои навыки выживания для создания полезных предметов.",
        "effect": "craft_item",
        "type": "positive",
        "items": {
            "energy_boost": {
                "name": "Энергетический напиток",
                "description": "Самодельный энергетик из местных растений",
                "effect": "max_energy",
                "value": 10
            },
            "health_boost": {
                "name": "Целебная мазь",
                "description": "Мазь из лечебных трав",
                "effect": "max_health",
                "value": 10
            },
            "speed_boost": {
                "name": "Стимулятор",
                "description": "Временный стимулятор из природных компонентов",
                "effect": "move_bonus",
                "value": 2,
                "duration": 3
            },
            "speed_penalty": {
                "name": "Тяжелый рюкзак",
                "description": "Дополнительные припасы замедляют движение",
                "effect": "move_penalty",
                "value": -2,
                "duration": 3
            }
        }
    },
    "mysterious_friend": {
        "name": "Таинственный друг",
        "description": "Вы получили перевод от таинственного друга!",
        "effect": "money",
        "value": (500, 1000),  # Диапазон случайной суммы
        "type": "positive"
    },

    # Нейтральные события (50)
    "weather_change": {
        "name": "Изменение погоды",
        "description": "Погода изменилась, но это не влияет на ваше путешествие.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "strange_noise": {
        "name": "Странный шум",
        "description": "Вы слышите странный шум в лесу, но решаете не сворачивать с пути.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "abandoned_camp": {
        "name": "Брошенный лагерь",
        "description": "Вы нашли следы чужого лагеря. Похоже, здесь недавно кто-то ночевал.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "distant_lights": {
        "name": "Огни вдалеке",
        "description": "Вы видите огни вдалеке, но решаете не сворачивать с пути.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "old_map": {
        "name": "Старая карта",
        "description": "Вы нашли старую карту, но она слишком изношена, чтобы быть полезной.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "animal_tracks": {
        "name": "Следы животных",
        "description": "Вы видите следы диких животных, но они не представляют угрозы.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "ruined_building": {
        "name": "Разрушенное здание",
        "description": "Вы нашли разрушенное здание. Когда-то здесь была деревня.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "strange_marks": {
        "name": "Странные отметки",
        "description": "Вы видите странные отметки на деревьях, но их значение неизвестно.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "distant_smoke": {
        "name": "Дым вдалеке",
        "description": "Вы видите дым вдалеке, но решаете не проверять его источник.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "old_campfire": {
        "name": "Старый костер",
        "description": "Вы нашли следы старого костра, но он давно остыл.",
        "effect": "none",
        "value": 0,
        "type": "neutral"
    },
    "meet_traveler": {
        "name": "Встреча с путешественником",
        "description": "Вы встретили другого путешественника и обменялись историями!",
        "effect": "none"
    },
    "find_camp": {
        "name": "Найден лагерь",
        "description": "Вы нашли старый лагерь и отдохнули там!",
        "effect": "energy",
        "value": 10
    },

    # Негативные события (50)
    "sun_hell": {
        "name": "Солнечный ад",
        "description": "Жара становится невыносимой. Вы расходуете больше энергии на поиск тени и воды.",
        "effect": "energy_cost",
        "value": 15,
        "type": "negative"
    },
    "heavy_rain": {
        "name": "Проливной дождь",
        "description": "Дождь мешает вам идти. Дорога стала скользкой, а одежда промокла.",
        "effect": "energy_cost",
        "value": 15,
        "type": "negative"
    },
    "cold_night": {
        "name": "Ночные холода",
        "description": "Ночью было очень холодно, вы плохо спали и утром чувствуете усталость.",
        "effect": "energy_cost",
        "value": 15,
        "type": "negative"
    },
    "survival": {
        "name": "Выживание на подножном корме",
        "description": "У вас закончилась еда. Приходится питаться насекомыми и дождевыми червями. Это безопасно, но дает мало энергии.",
        "effect": "energy",
        "value": 10,
        "type": "negative"
    },
    "injury": {
        "name": "Травма",
        "description": "Вы подвернули ногу!",
        "effect": "injury",
        "value": 2,
        "move_penalty": -1
    },
    "dog_injury": {
        "name": "Травма собаки",
        "description": "Ваша собака поранила лапу о острый камень.",
        "effect": "dog_health",
        "value": -15,
        "type": "negative"
    },
    "player_injury": {
        "name": "Падение",
        "description": "Вы поскользнулись на мокрой дороге и упали.",
        "effect": "player_health",
        "value": -15,
        "type": "negative"
    },
    "food_poisoning": {
        "name": "Отравление",
        "description": "Вы съели что-то несвежее и отравились.",
        "effect": "player_health",
        "value": -20,
        "type": "negative"
    },
    "dog_illness": {
        "name": "Болезнь собаки",
        "description": "Ваша собака подхватила инфекцию от грязной воды.",
        "effect": "dog_health",
        "value": -20,
        "type": "negative"
    },
    "bandit_attack": {
        "name": "Нападение бандитов",
        "description": "На вас напали бандиты! Вы потеряли часть припасов и получили ранения.",
        "effect": "player_health",
        "value": -15,
        "type": "negative"
    },
    "swamp": {
        "name": "Болото",
        "description": "Вы заблудились в болотистой местности. Пришлось искать обходной путь.",
        "effect": "energy",
        "value": -25,
        "type": "negative"
    },
    "mountain_path": {
        "name": "Горная тропа",
        "description": "Крутой подъем отнял много сил. Пришлось идти медленнее.",
        "effect": "energy_cost",
        "value": 20,
        "type": "negative"
    },
    "dog_fight": {
        "name": "Схватка с дикой собакой",
        "description": "Ваша собака вступила в схватку с дикой собакой!",
        "effect": "dog_health",
        "value": -20,
        "type": "negative"
    },
    "broken_equipment": {
        "name": "Сломанное снаряжение",
        "description": "Ваше снаряжение сломалось, приходится нести его на себе.",
        "effect": "energy_cost",
        "value": 15,
        "type": "negative"
    },
    # Новые события для собаки
    "dog_food_poisoning": {
        "name": "Отравление",
        "description": "Собака нашла и съела испорченные объедки. Это может быть опасно для её здоровья!",
        "effect": "dog_health",
        "value": -10,
        "type": "negative"
    },
    "dog_exhaustion": {
        "name": "Переутомление",
        "description": "Собака сильно устала от долгого пути. Нужно дать ей отдохнуть!",
        "effect": "dog_health",
        "value": -5,
        "type": "negative"
    },
    "gas_station_food": {
        "name": "Еда на заправке",
        "description": "На заправке вы купили специальный корм для собак. Ваш питомец с удовольствием поел!",
        "effect": "dog_health",
        "value": 5,
        "type": "positive"
    },
    "stranger_food": {
        "name": "Добрый странник",
        "description": "Встреченный странник поделился своей едой с вашей собакой. Она выглядит довольной!",
        "effect": "dog_health",
        "value": 10,
        "type": "positive"
    },
    "dog_sick": {
        "name": "Собака заболела",
        "description": "Ваша собака чувствует себя плохо!",
        "effect": "dog_health",
        "value": -15
    },
    "bad_weather": {
        "name": "Плохая погода",
        "description": "Дождь и ветер замедляют ваше движение!",
        "effect": "move_penalty",
        "value": -1
    },
    "telegram_donation": {
        "name": "Донат от подписчиков",
        "description": "Ваши подписчики в Telegram поддержали ваше путешествие!",
        "effect": "money",
        "value": (1, 100)  # Случайная сумма от 1 до 100
    },
    "sponsor_deal": {
        "name": "Спонсорский контракт",
        "description": "Местная компания предложила спонсорство!",
        "effect": "money",
        "value": (50, 200)  # Случайная сумма от 50 до 200
    },
    "merch_sales": {
        "name": "Продажа мерча",
        "description": "Вы продали футболки с логотипом вашего путешествия!",
        "effect": "money",
        "value": (30, 150)  # Случайная сумма от 30 до 150
    },
    "stream_donation": {
        "name": "Донат на стриме",
        "description": "Зрители вашего стрима поддержали путешествие!",
        "effect": "money",
        "value": (20, 100)  # Случайная сумма от 20 до 100
    },
    "ad_revenue": {
        "name": "Доход от рекламы",
        "description": "Вы получили оплату за рекламу в вашем блоге!",
        "effect": "money",
        "value": (40, 180)  # Случайная сумма от 40 до 180
    }
} 