CITIES = {
    0: "Самара",
    22: "Жигулёвск",
    36: "Сызрань",
    53: "Новоспасское",
    64: "Кузнецк",
    86: "Пенза",
    106: "Нижний Ломов",
    126: "Зубова Поляна",
    142: "Шацк",
    174: "Рязань",
    192: "Коломна",
    202: "Бронницы",
    210: "Люберцы",
    220: "Москва"
}

def get_city_at_position(position):
    """Возвращает название города на указанной позиции или None, если города нет"""
    return CITIES.get(position)

def get_next_city(position):
    """Возвращает название и позицию следующего города после указанной позиции"""
    next_positions = sorted([pos for pos in CITIES.keys() if pos > position])
    if next_positions:
        next_pos = next_positions[0]
        return CITIES[next_pos], next_pos
    return None, None

def get_previous_city(position):
    """Возвращает название и позицию предыдущего города до указанной позиции"""
    prev_positions = sorted([pos for pos in CITIES.keys() if pos < position], reverse=True)
    if prev_positions:
        prev_pos = prev_positions[0]
        return CITIES[prev_pos], prev_pos
    return None, None 