from func import *

ally_guild = 392532665

func.omicron_skills = func.get_skill_list()  # Получаем список скиллов
guild = func.get_guild(ally_guild)  # Получаем информацию о гильдии
players_ally = func.get_players(guild)  # Получаем список игроков гильдии
players = func.get_players_info(players_ally)  # Получаем информацию о игроках гильдии
for player in players:
    print(f"Проверка игрока: {player['name']}...")
    if func.user_exist(player):  # Если пользовать уже есть в БД
        old_roster = func.get_roster(player['allyCode'])  # Получаем список персонажей игрока из БД
        func.roster_updated(player, old_roster)  # Сверяем персонажей
    else:
        func.add_user(player)  # Добавляем игрока в БД
