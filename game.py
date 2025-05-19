import random
import json
import os
from events import EVENTS
from cities import get_city_at_position, get_next_city, get_previous_city, CITIES
from mini_games import MINI_GAMES, play_mini_game
from achievements import ACHIEVEMENTS

# Список городов с магазинами
SHOP_CITIES = ["Самара", "Сызрань", "Пенза", "Рязань", "Москва"]

# Товары в магазине
SHOP_ITEMS = {
    "Аптечка": {"buy": 300, "sell": 200, "effect": "health", "value": 30},
    "Вода": {"buy": 150, "sell": 100, "effect": "energy", "value": 20},
    "Еда": {"buy": 150, "sell": 100, "effect": "energy", "value": 25}
}

# Мини-игры (блогерство)
BLOGGING_ACTIVITIES = {
    "Стрим": {
        "description": "Проведите стрим о своем путешествии",
        "energy_cost": 30,
        "donation_range": (50, 200)
    },
    "Видео": {
        "description": "Снимите видео о своем путешествии",
        "energy_cost": 40,
        "donation_range": (100, 300)
    },
    "NFT": {
        "description": "Выпустите новую коллекцию NFT",
        "energy_cost": 50,
        "donation_range": (200, 500)
    }
}

def save_game(game_data, username):
    """Сохраняет игру в файл"""
    if not os.path.exists('saves'):
        os.makedirs('saves')
    
    with open(f'saves/{username}.json', 'w', encoding='utf-8') as f:
        json.dump(game_data, f, ensure_ascii=False, indent=4)

def load_game(username):
    """Загружает игру из файла"""
    try:
        with open(f'saves/{username}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_save_data(game):
    """Получает данные для сохранения из объекта игры"""
    return {
        "player_position": game.player_position,
        "player_health": game.player_health,
        "player_energy": game.player_energy,
        "dog_health": game.dog_health,
        "injury_turns": game.injury_turns,
        "last_city": game.last_city,
        "next_city": game.next_city,
        "distance_to_next_city": game.distance_to_next_city,
        "rested_in_city": game.rested_in_city,
        "skip_next_turn": game.skip_next_turn,
        "active_effects": game.active_effects,
        "money": game.money,
        "inventory": game.inventory,
        "turn_count": game.turn_count,
        "dog_abscess": game.dog_abscess,
        "games_won": game.games_won,
        "monetization_earnings": game.monetization_earnings,
        "donations_received": game.donations_received,
        "sponsor_deals": game.sponsor_deals,
        "achievements": game.achievements
    }

def load_save_data(game, save_data):
    """Загружает данные сохранения в объект игры"""
    game.player_position = save_data["player_position"]
    game.player_health = save_data["player_health"]
    game.player_energy = save_data["player_energy"]
    game.dog_health = save_data["dog_health"]
    game.injury_turns = save_data["injury_turns"]
    game.last_city = save_data["last_city"]
    game.next_city = save_data["next_city"]
    game.distance_to_next_city = save_data["distance_to_next_city"]
    game.rested_in_city = save_data["rested_in_city"]
    game.skip_next_turn = save_data["skip_next_turn"]
    game.active_effects = save_data["active_effects"]
    game.money = save_data["money"]
    game.inventory = save_data["inventory"]
    game.turn_count = save_data["turn_count"]
    game.dog_abscess = save_data["dog_abscess"]
    game.games_won = save_data["games_won"]
    game.monetization_earnings = save_data["monetization_earnings"]
    game.donations_received = save_data["donations_received"]
    game.sponsor_deals = save_data["sponsor_deals"]
    game.achievements = save_data["achievements"]

def print_message(title, content):
    """Выводит сообщение без рамок"""
    print(f"\n{title}")
    print("-" * len(title))
    for line in content:
        print(line)
    print()

class Game:
    def __init__(self, username=None):
        self.username = username
        self.player_position = 0
        self.player_health = 100
        self.player_energy = 100
        self.dog_health = 100
        self.injury_turns = 0
        self.last_city = None
        self.next_city = None
        self.distance_to_next_city = 0
        self.rested_in_city = False
        self.skip_next_turn = False
        self.active_effects = {}
        self.money = 50
        self.inventory = {
            "Аптечка": 1,
            "Еда": 1,
            "Вода": 1
        }
        self.turn_count = 0
        self.dog_abscess = 0
        self.games_won = 0
        self.monetization_earnings = 0
        self.donations_received = 0
        self.sponsor_deals = 0
        self.achievements = ACHIEVEMENTS.copy()

    def get_inventory_slots(self):
        """Возвращает количество доступных слотов инвентаря"""
        return 12 if self.dog_health > 50 else 10

    def get_inventory_size(self):
        """Возвращает текущий размер инвентаря"""
        return sum(self.inventory.values())

    def show_shop_menu(self):
        content = [
            f"Ваши деньги: {self.money} JK",
            f"Слоты инвентаря: {self.get_inventory_size()}/{self.get_inventory_slots()}",
            "",
            "Товары:"
        ]
        for i, (item, data) in enumerate(SHOP_ITEMS.items(), 1):
            effect_text = ""
            if data["effect"] == "health":
                effect_text = f"(+{data['value']} здоровья)"
            elif data["effect"] == "energy":
                effect_text = f"(+{data['value']} энергии)"
            content.append(f"{i}. {item} - {data['buy']} JK (продажа: {data['sell']} JK) {effect_text}")
        content.append(f"{len(SHOP_ITEMS) + 1}. Выход")
        
        print_message("Магазин", content)

        while True:
            choice = input("\nВыберите действие (купить/продать номер_товара или выход): ").lower()
            if choice == "выход":
                break

            try:
                action, item_num = choice.split()
                item_num = int(item_num)
                if 1 <= item_num <= len(SHOP_ITEMS):
                    item_name = list(SHOP_ITEMS.keys())[item_num - 1]
                    if action == "купить":
                        if self.money >= SHOP_ITEMS[item_name]["buy"]:
                            if self.get_inventory_size() < self.get_inventory_slots():
                                self.money -= SHOP_ITEMS[item_name]["buy"]
                                self.inventory[item_name] = self.inventory.get(item_name, 0) + 1
                                print_message("Покупка", [f"Вы купили {item_name}!"])
                            else:
                                print_message("Ошибка", ["Инвентарь полон!"])
                        else:
                            print_message("Ошибка", ["Недостаточно денег!"])
                    elif action == "продать":
                        if item_name in self.inventory and self.inventory[item_name] > 0:
                            self.money += SHOP_ITEMS[item_name]["sell"]
                            self.inventory[item_name] -= 1
                            if self.inventory[item_name] == 0:
                                del self.inventory[item_name]
                            print_message("Продажа", [f"Вы продали {item_name}!"])
                        else:
                            print_message("Ошибка", ["У вас нет этого предмета!"])
                else:
                    print_message("Ошибка", ["Неверный номер товара!"])
            except ValueError:
                print_message("Ошибка", ["Неверный формат команды!"])

    def use_item(self, item_name):
        if item_name not in self.inventory or self.inventory[item_name] <= 0:
            print_message("Ошибка", ["У вас нет этого предмета!"])
            return

        if item_name == "Аптечка":
            print_message("Использование аптечки", [
                "Выберите действие:",
                "1. Применить на себе (+30 здоровья)",
                "2. Применить на собаке (+30 здоровья)",
                "3. Выбросить"
            ])
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.player_health = min(100, self.player_health + 30)
                print_message("Использование", ["Вы восстановили 30 здоровья!"])
            elif choice == "2":
                self.dog_health = min(100, self.dog_health + 30)
                print_message("Использование", ["Собака восстановила 30 здоровья!"])
            elif choice == "3":
                print_message("Выброшено", ["Вы выбросили аптечку"])
            else:
                print_message("Ошибка", ["Неверный выбор!"])
                return
        elif item_name == "Вода":
            print_message("Использование воды", [
                "Выберите действие:",
                "1. Выпить самим (+20 энергии)",
                "2. Дать собаке (+3 здоровья)",
                "3. Выбросить"
            ])
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.player_energy = min(100, self.player_energy + 20)
                print_message("Использование", ["Вы восстановили 20 энергии!"])
            elif choice == "2":
                self.dog_health = min(100, self.dog_health + 3)
                print_message("Использование", ["Собака восстановила 3 здоровья!"])
            elif choice == "3":
                print_message("Выброшено", ["Вы выбросили воду"])
            else:
                print_message("Ошибка", ["Неверный выбор!"])
                return
        elif item_name == "Еда":
            print_message("Использование еды", [
                "Выберите действие:",
                "1. Съесть самим (+25 энергии)",
                "2. Дать собаке (+5 здоровья)",
                "3. Выбросить"
            ])
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.player_energy = min(100, self.player_energy + 25)
                print_message("Использование", ["Вы восстановили 25 энергии!"])
            elif choice == "2":
                self.dog_health = min(100, self.dog_health + 5)
                print_message("Использование", ["Собака восстановила 5 здоровья!"])
            elif choice == "3":
                print_message("Выброшено", ["Вы выбросили еду"])
            else:
                print_message("Ошибка", ["Неверный выбор!"])
                return

        self.inventory[item_name] -= 1
        if self.inventory[item_name] == 0:
            del self.inventory[item_name]

    def show_inventory_menu(self):
        if not self.inventory:
            print_message("Инвентарь", ["У вас нет предметов!"])
            return

        content = [
            f"Слоты инвентаря: {self.get_inventory_size()}/{self.get_inventory_slots()}",
            "Ваши предметы:"
        ]
        for i, (item, count) in enumerate(self.inventory.items(), 1):
            effect_text = ""
            if item in SHOP_ITEMS:
                if SHOP_ITEMS[item]["effect"] == "health":
                    effect_text = f" (+{SHOP_ITEMS[item]['value']} здоровья)"
                elif SHOP_ITEMS[item]["effect"] == "energy":
                    effect_text = f" (+{SHOP_ITEMS[item]['value']} энергии)"
            content.append(f"{i}. {item} (x{count}){effect_text}")
        content.append(f"{len(self.inventory) + 1}. Выход")
        
        print_message("Инвентарь", content)

        while True:
            choice = input("\nВыберите предмет для использования (или выход): ")
            if choice == str(len(self.inventory) + 1) or choice.lower() in ['выход', 'exit']:
                break

            try:
                item_num = int(choice)
                if 1 <= item_num <= len(self.inventory):
                    item_name = list(self.inventory.keys())[item_num - 1]
                    self.use_item(item_name)
                else:
                    print_message("Ошибка", ["Неверный номер предмета!"])
            except ValueError:
                print_message("Ошибка", ["Неверный формат команды!"])

    def show_jobs_menu(self):
        content = [
            "Доступные подработки:",
            ""
        ]
        
        for i, (job_name, job_data) in enumerate(JOBS.items(), 1):
            can_work, reason = check_job_requirements(
                job_data, 
                self.player_health, 
                self.player_energy, 
                self.dog_health
            )
            
            status = "✓" if can_work else f"✗ ({reason})"
            content.append(f"{i}. {job_name} - {job_data['description']} {status}")
            content.append(f"   Энергия: -{job_data['energy_cost']}, Зарплата: {job_data['money'][0]}-{job_data['money'][1]} JK")
            content.append("")
        
        content.append(f"{len(JOBS) + 1}. Выход")
        print_message("Подработки", content)
        
        while True:
            choice = input("\nВыберите работу (или выход): ")
            if choice == str(len(JOBS) + 1) or choice.lower() in ['выход', 'exit']:
                break
                
            try:
                job_num = int(choice)
                if 1 <= job_num <= len(JOBS):
                    job_name = list(JOBS.keys())[job_num - 1]
                    job_data = JOBS[job_name]
                    
                    can_work, reason = check_job_requirements(
                        job_data, 
                        self.player_health, 
                        self.player_energy, 
                        self.dog_health
                    )
                    
                    if can_work:
                        self.player_energy -= job_data["energy_cost"]
                        reward = get_job_reward(job_data)
                        self.money += reward
                        self.games_won += 1
                        
                        print_message("Работа", [
                            f"Вы выполнили работу '{job_name}'",
                            f"Получено: {reward} JK",
                            f"Потрачено энергии: {job_data['energy_cost']}"
                        ])
                        
                        # Проверяем достижения
                        achievement_reward = self.check_achievements()
                        
                        if achievement_reward > 0:
                            self.money += achievement_reward
                            print_message("Достижение", [
                                "Вы получили награду за достижение!",
                                f"+{achievement_reward} JK"
                            ])
                    else:
                        print_message("Ошибка", [reason])
                else:
                    print_message("Ошибка", ["Неверный номер работы!"])
            except ValueError:
                print_message("Ошибка", ["Неверный формат команды!"])

    def show_blogging_menu(self):
        content = [
            "Доступные активности:",
            ""
        ]
        
        for i, (activity_name, activity_data) in enumerate(BLOGGING_ACTIVITIES.items(), 1):
            if self.player_energy < activity_data["energy_cost"]:
                status = f"✗ (Недостаточно энергии: {self.player_energy}/{activity_data['energy_cost']})"
            else:
                status = "✓"
                
            content.append(f"{i}. {activity_name} - {activity_data['description']} {status}")
            content.append(f"   Энергия: -{activity_data['energy_cost']}")
            content.append(f"   Возможные донаты: {activity_data['donation_range'][0]}-{activity_data['donation_range'][1]} JK")
            content.append("")
        
        content.append(f"{len(BLOGGING_ACTIVITIES) + 1}. Выход")
        print_message("Блогерство", content)
        
        while True:
            choice = input("\nВыберите активность (или выход): ")
            if choice == str(len(BLOGGING_ACTIVITIES) + 1) or choice.lower() in ['выход', 'exit']:
                current_city = get_city_at_position(self.player_position)
                if current_city:
                    self.show_city_menu(current_city)
                return
                
            try:
                activity_num = int(choice)
                if 1 <= activity_num <= len(BLOGGING_ACTIVITIES):
                    activity_name = list(BLOGGING_ACTIVITIES.keys())[activity_num - 1]
                    activity_data = BLOGGING_ACTIVITIES[activity_name]
                    
                    if self.player_energy < activity_data["energy_cost"]:
                        print_message("Ошибка", ["Недостаточно энергии!"])
                        continue
                        
                    self.player_energy -= activity_data["energy_cost"]
                    won, result = play_mini_game(activity_data)
                    
                    if won:
                        self.money += result
                        self.donations_received += 1
                        self.monetization_earnings += result
                            
                        print_message("Успех", [
                            f"Вы получили {result} JK!"
                        ])
                    else:
                        if activity_name == "Стрим":
                            print_message("Неудача", [
                                "Стрим вы провели, но вам не донатили!"
                            ])
                        elif activity_name == "Видео":
                            print_message("Неудача", [
                                "Видео не набрало просмотров!"
                            ])
                        elif activity_name == "NFT":
                            print_message("Неудача", [
                                "Коллекция NFT не вызвала интереса!"
                            ])
                    
                    # Проверяем достижения
                    achievement_reward = self.check_achievements()
                    if achievement_reward > 0:
                        self.money += achievement_reward
                        print_message("Достижение", [
                            "Вы получили награду за достижение!",
                            f"+{achievement_reward} JK"
                        ])
                else:
                    print_message("Ошибка", ["Неверный номер активности!"])
            except ValueError:
                print_message("Ошибка", ["Неверный формат команды!"])

    def show_achievements_menu(self):
        content = [
            "Ваши достижения:",
            ""
        ]
        
        for achievement_name, achievement_data in self.achievements.items():
            status = "✓" if achievement_data["completed"] else "✗"
            if "progress" in achievement_data:
                progress = f" ({achievement_data['progress']}/10)" if achievement_data["progress"] > 0 else ""
            else:
                progress = ""
            content.append(f"{status} {achievement_name}{progress}")
            content.append(f"   {achievement_data['description']}")
            content.append(f"   Награда: {achievement_data['reward']} JK")
            content.append("")
        
        print_message("Достижения", content)
        input("\nНажмите Enter для продолжения...")

    def show_city_menu(self, current_city):
        content = [
            f"Вы находитесь в городе {current_city}",
            "",
            "Доступные здания:",
            "1. Магазин",
            "2. Отдых",
            "3. Блогерство",
            "4. Достижения",
            "5. Сохранить игру"
        ]
        
        # Добавляем ветеринарную станцию для Кузнецка и Рязани
        if current_city in ["Кузнецк", "Рязань"]:
            content.append("6. Ветеринарная станция")
            content.append("7. Выйти из города")
        else:
            content.append("6. Выйти из города")
        
        print_message("Город", content)
        
        while True:
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.show_shop_menu()
            elif choice == "2":
                self.rest()
            elif choice == "3":
                self.show_blogging_menu()
            elif choice == "4":
                self.show_achievements_menu()
            elif choice == "5":
                save_game(get_save_data(self), self.username)
                print_message("Сохранение", ["Игра успешно сохранена!"])
            elif choice == "6" and current_city in ["Кузнецк", "Рязань"]:
                if self.dog_health < 100:
                    cost = (100 - self.dog_health) * 5
                    if self.money >= cost:
                        self.money -= cost
                        old_health = self.dog_health
                        self.dog_health = 100
                        print_message("Ветеринарная станция", [
                            f"Ветеринарная служба вылечила собаку!",
                            f"Стоимость лечения: {cost} JK",
                            f"Здоровье собаки: {old_health} → 100 (+{100 - old_health})"
                        ])
                    else:
                        print_message("Ветеринарная станция", [
                            f"Недостаточно денег для лечения!",
                            f"Необходимо: {cost} JK",
                            f"У вас: {self.money} JK"
                        ])
                else:
                    print_message("Ветеринарная станция", ["Собака полностью здорова!"])
            elif choice in ["6", "7"]:
                break
            else:
                print_message("Ошибка", ["Неверный выбор!"])

    def move_player(self, special_move=None):
        skip_turn = self.skip_next_turn
        self.skip_next_turn = False
        
        # Проверяем абсцесс у собаки
        if self.dog_abscess > 0:
            self.dog_health = max(0, self.dog_health - 7)
            self.dog_abscess -= 1
            if self.dog_health <= 0:
                print_message("Трагедия", ["Ваша собака погибла от абсцесса!"])
                self.dog_health = 0
            elif self.dog_abscess == 0:
                print_message("Выздоровление", ["Абсцесс у собаки наконец-то прошел!"])
            else:
                print_message("Абсцесс", [f"Абсцесс у собаки все еще беспокоит! Осталось ходов: {self.dog_abscess}"])
                # Показываем прогноз потери здоровья
                remaining_health = self.dog_health - (7 * self.dog_abscess)
                print_message("Прогноз здоровья", [
                    f"Текущее здоровье: {self.dog_health}",
                    f"Прогноз через {self.dog_abscess} ходов: {max(0, remaining_health)}",
                    f"Потеря здоровья за ход: -7"
                ])

        if skip_turn:
            # Сохраняем старые значения параметров
            old_energy = self.player_energy
            old_health = self.player_health
            old_dog_health = self.dog_health
            
            # Восстанавливаем параметры как при отдыхе
            self.player_energy = min(100, self.player_energy + 20)
            self.player_health = min(100, self.player_health + 10)
            
            content = [
                "Вы должны пропустить этот ход из-за последствий Рывка Анаконды!",
                "",
                "Во время отдыха:",
                f"Энергия: {old_energy} → {self.player_energy} (+{self.player_energy - old_energy})",
                f"Здоровье: {old_health} → {self.player_health} (+{self.player_health - old_health})"
            ]
            print_message("Пропуск хода", content)
            return

        if self.injury_turns > 0:
            print_message("Травма", ["Вы ранены и должны пропустить ход!"])
            self.injury_turns -= 1
            if self.injury_turns == 0:
                print_message("Выздоровление", ["Вы восстановились после травмы!"])
                self.player_health = min(100, self.player_health + 20)
                self.player_energy = min(100, self.player_energy + 20)
            return

        # Случайное событие при движении
        event_message = []
        
        # Получаем случайное событие из всех доступных событий
        all_events = list(EVENTS.items())
        random_event = random.choice(all_events)
        event_id, event_data = random_event
        
        event_message.extend([
            "СОБЫТИЕ",
            "-------",
            f"Название: {event_data['name']}",
            f"Описание: {event_data['description']}",
            ""
        ])
        
        # Применяем эффекты события
        if event_data['effect'] != 'none':
            if event_data['effect'] == 'player_health':
                self.player_health = max(0, min(100, self.player_health + event_data['value']))
            elif event_data['effect'] == 'energy':
                self.player_energy = max(0, min(100, self.player_energy + event_data['value']))
            elif event_data['effect'] == 'dog_health':
                self.dog_health = max(0, min(100, self.dog_health + event_data['value']))
                # Показываем прогноз здоровья собаки на 5 ходов вперед
                if event_data['value'] < 0:  # Если это негативное событие
                    event_message.extend([
                        f"Текущее здоровье собаки: {self.dog_health}",
                        f"Потеря здоровья: {abs(event_data['value'])}",
                        f"Здоровье после события: {max(0, self.dog_health)}",
                        ""
                    ])
            elif event_data['effect'] == 'money':
                if isinstance(event_data['value'], tuple):
                    value = random.randint(event_data['value'][0], event_data['value'][1])
                else:
                    value = event_data['value']
                self.money = max(0, self.money + value)
                event_message.extend([
                    f"Получено денег: {value} JK",
                    f"Текущий баланс: {self.money} JK",
                    ""
                ])
            elif event_data['effect'] == 'special_move':
                if self.player_energy >= event_data.get('energy_cost', 0):
                    self.player_energy -= event_data['energy_cost']
                    if event_data.get('health_cost'):
                        self.player_health = max(0, self.player_health - event_data['health_cost'])
                    if event_data.get('skip_turn'):
                        self.skip_next_turn = True
            elif event_data['effect'] == 'injury':
                self.injury_turns = event_data['value']
                if event_data.get('move_penalty'):
                    self.active_effects['move_penalty'] = {
                        'value': event_data['move_penalty'],
                        'duration': event_data['value']
                    }
            elif event_data['effect'] == 'energy_cost':
                self.active_effects['energy_cost'] = {
                    'value': event_data['value'],
                    'duration': 1
                }
            elif event_data['effect'] == 'bonus_move':
                self.active_effects['move_bonus'] = {
                    'value': event_data['value'],
                    'duration': 1
                }
            
            event_message.append("Событие повлияло на ваши параметры!")
            
            # Добавляем информацию об изменениях инвентаря
            if event_data['name'] == "Добрые жители":
                if self.get_inventory_size() < self.get_inventory_slots():
                    self.inventory["Еда"] = self.inventory.get("Еда", 0) + 1
                    event_message.append(f"Что произошло: +1 еда в инвентаре ({self.get_inventory_slots() - self.get_inventory_size()}/{self.get_inventory_slots()} свободно)")
                else:
                    event_message.append("Что произошло: инвентарь полон, еда потеряна")

        # Добавляем разделитель между событием и движением
        event_message.extend([
            "",
            "ДВИЖЕНИЕ",
            "--------"
        ])

        move_distance = 4

        # Создаем копию словаря для безопасной итерации
        effects_to_remove = []
        for effect, data in self.active_effects.items():
            if data["duration"] > 0:
                if effect == "move_bonus":
                    move_distance += data["value"]
                elif effect == "move_penalty":
                    move_distance += data["value"]
                data["duration"] -= 1
                if data["duration"] == 0:
                    effects_to_remove.append(effect)
        
        # Удаляем истекшие эффекты после итерации
        for effect in effects_to_remove:
            del self.active_effects[effect]

        if special_move == "cobra_throw":
            if self.player_energy >= 35:
                move_distance = 8
                self.player_energy -= 35
                event_message.append(f"Вы использовали Бросок Кобры и прошли {move_distance} клеток!")
            else:
                print_message("Ошибка", ["Недостаточно энергии для Броска Кобры!"])
                return
        elif special_move == "anaconda_rush":
            if self.player_energy >= 70 and self.player_health >= 20:
                move_distance = 12
                self.player_energy -= 70
                self.player_health -= 20
                self.skip_next_turn = True
                self.active_effects["move_penalty"] = {"value": -1, "duration": 1}
                event_message.extend([
                    f"Вы использовали Рывок Анаконды и прошли {move_distance} клеток!",
                    "Вы потеряли 20 здоровья и должны пропустить следующий ход!"
                ])
            else:
                print_message("Ошибка", ["Недостаточно энергии или здоровья для Рывка Анаконды!"])
                return

        if self.rested_in_city and random.random() < 0.1:
            move_distance += 1
            event_message.append("Эффект 'С новыми силами' позволил вам пройти на 1 клетку дальше!")

        next_city_info = get_next_city(self.player_position)
        if next_city_info and next_city_info[1] - self.player_position <= move_distance:
            event_message.append(f"Впереди город {next_city_info[0]} ({next_city_info[1] - self.player_position} кл.)")
            choice = input("Хотите зайти в город? (да/нет): ").lower()
            if choice in ['да', 'yes', 'y', 'д']:
                move_distance = next_city_info[1] - self.player_position

        energy_cost = 20
        if self.player_energy < energy_cost:
            health_cost = energy_cost - self.player_energy
            self.player_health -= health_cost
            self.player_energy = 0
            event_message.append(f"Недостаточно энергии! Потеряно {health_cost} здоровья.")
        else:
            self.player_energy -= energy_cost

        old_position = self.player_position
        self.player_position += move_distance
        event_message.append(f"Вы прошли {move_distance} клеток (с {old_position} на {self.player_position})")

        current_city = get_city_at_position(self.player_position)
        if current_city:
            event_message.append(f"Вы достигли города {current_city}!")
            self.last_city = current_city
            next_city_info = get_next_city(self.player_position)
            if next_city_info:
                self.next_city = next_city_info[0]
                self.distance_to_next_city = next_city_info[1] - self.player_position
                event_message.append(f"До следующего города {self.next_city} осталось {self.distance_to_next_city} клеток")
            else:
                self.next_city = None
                self.distance_to_next_city = 0
                event_message.append("Это последний город на пути!")

            # Добавляем информацию о текущем состоянии
            event_message.extend([
                "",
                "Текущее состояние:",
                f"Энергия: {self.player_energy}/100",
                f"Здоровье: {self.player_health}/100",
                f"Здоровье собаки: {self.dog_health}/100",
                f"Деньги: {self.money} JK"
            ])

            # Показываем все сообщения одним блоком
            print_message("Ход", event_message)
            
            self.show_city_menu(current_city)
        else:
            # Добавляем информацию о текущем состоянии
            event_message.extend([
                "",
                "Текущее состояние:",
                f"Энергия: {self.player_energy}/100",
                f"Здоровье: {self.player_health}/100",
                f"Здоровье собаки: {self.dog_health}/100",
                f"Деньги: {self.money} JK"
            ])

            # Показываем все сообщения одним блоком
            print_message("Ход", event_message)

        # Проверяем здоровье собаки и обновляем инвентарь если нужно
        if self.dog_health <= 50 and self.get_inventory_size() > 10:
            # Оставляем только первые 10 предметов
            items_to_keep = list(self.inventory.items())[:10]
            self.inventory = dict(items_to_keep)
            print_message("Инвентарь", [
                "Здоровье собаки упало ниже 50%!",
                "Из-за этого вы потеряли часть предметов из инвентаря.",
                f"Осталось слотов: {self.get_inventory_slots()}"
            ])

    def show_special_abilities_menu(self):
        content = [
            "1. Бросок Кобры (8 кл., 35 энергии)",
            "2. Рывок Анаконды (12 кл., 70 энергии, -20 здоровья, пропуск хода)",
            "3. Назад"
        ]
        print_message("Специальные способности", content)

        choice = input("\nВыберите способность: ")
        if choice == "1":
            self.move_player("cobra_throw")
        elif choice == "2":
            self.move_player("anaconda_rush")
        elif choice == "3":
            return
        else:
            print_message("Ошибка", ["Неверный выбор!"])

    def display_status(self):
        content = [
            f"Ход: {self.turn_count}",
            f"Позиция: {self.player_position} кл.",
            ""
        ]
        
        current_city = get_city_at_position(self.player_position)
        if current_city:
            content.append(f"Город: {current_city}")
        else:
            if self.next_city:
                content.append(f"До следующего города {self.next_city}: {self.distance_to_next_city} кл.")
            if self.last_city:
                prev_city_info = get_previous_city(self.player_position)
                if prev_city_info:
                    content.append(f"От города {prev_city_info[0]}: {self.player_position - prev_city_info[1]} кл.")

        content.extend([
            "",
            "Параметры:",
            f"Энергия: {self.player_energy}/100",
            f"Здоровье: {self.player_health}/100",
            f"Здоровье собаки: {self.dog_health}/100",
            f"Деньги: {self.money} JK"
        ])
        
        if self.inventory:
            content.extend([
                "",
                f"Инвентарь ({self.get_inventory_size()}/{self.get_inventory_slots()}):"
            ])
            for item, count in dict(self.inventory).items():
                effect_text = ""
                if item in SHOP_ITEMS:
                    if SHOP_ITEMS[item]["effect"] == "health":
                        effect_text = f" (+{SHOP_ITEMS[item]['value']} здоровья)"
                    elif SHOP_ITEMS[item]["effect"] == "energy":
                        effect_text = f" (+{SHOP_ITEMS[item]['value']} энергии)"
                content.append(f"- {item}: {count}{effect_text}")

        if self.injury_turns > 0:
            content.extend([
                "",
                f"Травма: {self.injury_turns} ходов до выздоровления"
            ])
        
        if self.active_effects:
            content.extend([
                "",
                "Активные эффекты:"
            ])
            for effect, data in dict(self.active_effects).items():
                if data["duration"] > 0:
                    if effect == "move_bonus":
                        content.append(f"+{data['value']} к дальности хода ({data['duration']} ходов)")
                    elif effect == "move_penalty":
                        content.append(f"{data['value']} к дальности хода ({data['duration']} ходов)")

        content.extend([
            "",
            "Действия:",
            "1. Идти вперед (4 кл., 20 энергии)",
            "2. Специальные способности",
            "3. Отдых",
            "4. Инвентарь",
            "5. Выход"
        ])
        
        print_message("Статус", content)

    def rest(self):
        current_city = get_city_at_position(self.player_position)
        if current_city:
            # Сохраняем старые значения параметров
            old_energy = self.player_energy
            old_health = self.player_health
            old_dog_health = self.dog_health
            
            content = [
                f"Вы отдыхаете в городе {current_city}"
            ]
            self.player_energy = min(100, self.player_energy + 30)
            self.player_health = min(100, self.player_health + 20)
            self.rested_in_city = True
            
            # Добавляем информацию об изменениях
            content.extend([
                "",
                f"Энергия: {old_energy} → {self.player_energy} (+{self.player_energy - old_energy})",
                f"Здоровье: {old_health} → {self.player_health} (+{self.player_health - old_health})"
            ])
            
            if current_city in ["Кузнецк", "Пенза"]:
                dog_heal = random.randint(30, 50)
                self.dog_health = min(100, self.dog_health + dog_heal)
                content.append(f"Здоровье собаки: {old_dog_health} → {self.dog_health} (+{dog_heal})")
                content.append(f"Ветеринар в {current_city} помог вашей собаке")
            print_message("Отдых", content)
        else:
            # Сохраняем старые значения параметров
            old_energy = self.player_energy
            old_health = self.player_health
            
            # Сначала увеличиваем энергию и здоровье
            self.player_energy = min(100, self.player_energy + 20)
            self.player_health = min(100, self.player_health + 10)
            self.rested_in_city = False
            
            content = [
                "Вы отдыхаете на природе",
                "",
                f"Энергия: {old_energy} → {self.player_energy} (+{self.player_energy - old_energy})",
                f"Здоровье: {old_health} → {self.player_health} (+{self.player_health - old_health})"
            ]
            print_message("Отдых", content)

    def check_achievements(self):
        total_reward = 0
        stats = {
            "player_position": self.player_position,
            "money": self.money,
            "games_won": self.games_won,
            "turn_count": self.turn_count,
            "dog_health": self.dog_health,
            "monetization_earnings": self.monetization_earnings,
            "donations_received": self.donations_received,
            "sponsor_deals": self.sponsor_deals
        }
        
        for achievement_name, achievement_data in self.achievements.items():
            if not achievement_data["completed"]:
                if achievement_data["check"](stats):
                    achievement_data["completed"] = True
                    total_reward += achievement_data["reward"]
                    print_message("Новое достижение!", [
                        f"Достижение разблокировано: {achievement_name}",
                        f"Описание: {achievement_data['description']}",
                        f"Награда: {achievement_data['reward']} JK"
                    ])
        
        return total_reward

def main():
    print_message("Добро пожаловать", [
        "Добро пожаловать в игру 'Путь к Москве'!",
        "Ваша цель - добраться из Самары до Москвы (220-я клетка)",
        "Каждая клетка примерно соответствует 5 км реального расстояния",
        "",
        "Города на пути:"
    ])
    
    for city, pos in CITIES.items():
        print(f"- {city} ({pos}-я клетка)")

    # Проверяем существующие сохранения
    if os.path.exists('saves'):
        saves = [f[:-5] for f in os.listdir('saves') if f.endswith('.json')]
        if saves:
            print("\nНайдены сохранения:")
            for i, save in enumerate(saves, 1):
                print(f"{i}. {save}")
            print(f"{len(saves) + 1}. Новая игра")
            
            choice = input("\nВыберите сохранение или новую игру: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(saves):
                    username = saves[choice - 1]
                    password = input("Введите пароль: ")
                    # TODO: Добавить проверку пароля
                    game = Game(username)
                    save_data = load_game(username)
                    if save_data:
                        load_save_data(game, save_data)
                else:
                    username = input("Придумайте имя героя: ")
                    password = input("Придумайте пароль: ")
                    # TODO: Сохранить пароль
                    game = Game(username)
            except ValueError:
                print_message("Ошибка", ["Неверный выбор!"])
                return
        else:
            username = input("Придумайте имя героя: ")
            password = input("Придумайте пароль: ")
            # TODO: Сохранить пароль
            game = Game(username)
    else:
        username = input("Придумайте имя героя: ")
        password = input("Придумайте пароль: ")
        # TODO: Сохранить пароль
        game = Game(username)

    while True:
        game.display_status()
        choice = input("\nВыберите действие: ")

        if choice == "1":
            game.move_player()
            game.turn_count += 1
        elif choice == "2":
            game.show_special_abilities_menu()
            game.turn_count += 1
        elif choice == "3":
            game.rest()
            game.turn_count += 1
        elif choice == "4":
            game.show_inventory_menu()
        elif choice == "5":
            save_game(get_save_data(game), game.username)
            print_message("Сохранение", ["Игра успешно сохранена!"])
        elif choice == "6":
            print_message("Прощание", ["Спасибо за игру!"])
            break
        else:
            print_message("Ошибка", ["Неверный выбор!"])

if __name__ == "__main__":
    main() 