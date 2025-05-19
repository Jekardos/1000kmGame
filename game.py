import random
from events import EVENTS
from cities import get_city_at_position, get_next_city, get_previous_city, CITIES

# Список городов с магазинами
SHOP_CITIES = ["Самара", "Сызрань", "Пенза", "Рязань", "Москва"]

# Товары в магазине
SHOP_ITEMS = {
    "Аптечка": {"buy": 200, "sell": 150, "effect": "health", "value": 30},
    "Вода": {"buy": 100, "sell": 70, "effect": "energy", "value": 20},
    "Еда": {"buy": 100, "sell": 70, "effect": "energy", "value": 25}
}

def print_message(title, content):
    """Выводит сообщение без рамок"""
    print(f"\n{title}")
    print("-" * len(title))
    for line in content:
        print(line)
    print()

class Game:
    def __init__(self):
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
        self.money = 100
        self.inventory = {}
        self.turn_count = 0
        self.dog_abscess = 0  # Добавляем счетчик ходов для абсцесса

    def show_shop_menu(self):
        content = [
            f"Ваши деньги: {self.money} JK",
            "",
            "Товары:"
        ]
        for i, (item, data) in enumerate(SHOP_ITEMS.items(), 1):
            content.append(f"{i}. {item} - {data['buy']} JK (продажа: {data['sell']} JK)")
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
                            self.money -= SHOP_ITEMS[item_name]["buy"]
                            self.inventory[item_name] = self.inventory.get(item_name, 0) + 1
                            print_message("Покупка", [f"Вы купили {item_name}!"])
                        else:
                            print_message("Ошибка", ["Недостаточно денег!"])
                    elif action == "продать":
                        if item_name in self.inventory and self.inventory[item_name] > 0:
                            self.money += SHOP_ITEMS[item_name]["sell"]
                            self.inventory[item_name] -= 1
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

        content = ["Ваши предметы:"]
        for i, (item, count) in enumerate(self.inventory.items(), 1):
            content.append(f"{i}. {item} (x{count})")
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

    def show_city_menu(self, current_city):
        content = [
            f"Вы находитесь в городе {current_city}",
            "",
            "Доступные здания:",
            "1. Магазин",
            "2. Отдых"
        ]
        
        # Добавляем ветеринарную станцию для Кузнецка и Рязани
        if current_city in ["Кузнецк", "Рязань"]:
            content.append("3. Ветеринарная станция")
        
        content.append("4. Выйти из города")
        
        print_message("Город", content)
        
        while True:
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.show_shop_menu()
            elif choice == "2":
                self.rest()
            elif choice == "3" and current_city in ["Кузнецк", "Рязань"]:
                if self.dog_health < 100:
                    self.dog_health = 100
                    print_message("Ветеринарная станция", ["Ветеринарная служба вылечила собаку!"])
                else:
                    print_message("Ветеринарная станция", ["Собака полностью здорова!"])
            elif choice == "4":
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
            print_message("Пропуск хода", ["Вы должны пропустить этот ход из-за последствий Рывка Анаконды!"])
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
        event_chance = random.random()
        event_message = []
        
        if event_chance < 0.6:  # 60% шанс события
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

        # Добавляем разделитель между событием и движением
        if event_chance < 0.6:
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
                "Инвентарь:"
            ])
            for item, count in dict(self.inventory).items():
                content.append(f"- {item}: {count}")

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
            
            content = [
                "Вы отдыхаете на природе",
                "",
                f"Энергия: {old_energy} → {self.player_energy} (+{self.player_energy - old_energy})",
                f"Здоровье: {old_health} → {self.player_health} (+{self.player_health - old_health})"
            ]
            self.player_energy = min(100, self.player_energy + 20)
            self.rested_in_city = False
            print_message("Отдых", content)

def main():
    game = Game()
    print_message("Добро пожаловать", [
        "Добро пожаловать в игру 'Путь к Москве'!",
        "Ваша цель - добраться из Самары до Москвы (220-я клетка)",
        "Каждая клетка примерно соответствует 5 км реального расстояния",
        "",
        "Города на пути:"
    ])
    
    for city, pos in CITIES.items():
        print(f"- {city} ({pos}-я клетка)")

    while True:
        game.display_status()
        choice = input("\nВыберите действие: ")

        if choice == "1":
            game.turn_count += 1
            game.move_player()
        elif choice == "2":
            game.turn_count += 1
            game.show_special_abilities_menu()
        elif choice == "3":
            game.turn_count += 1
            game.rest()
        elif choice == "4":
            game.show_inventory_menu()
        elif choice == "5":
            print_message("Прощание", ["Спасибо за игру!"])
            break
        else:
            print_message("Ошибка", ["Неверный выбор!"])

if __name__ == "__main__":
    main() 