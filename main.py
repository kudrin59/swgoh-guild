from func import *

interval = 60

while True:
    func.omicron_skills = func.get_skill_list()  # Получаем список скиллов
    clients = func.get_clients()  # Получаем список клиентов с БД
    for client in clients:
        client_id = client[0]
        client_ally = client[1]
        client_login = client[2]
        print(f"Работаем с пользователем: {client_login}")
        guild = func.get_guild(client_ally)  # Получаем информацию о гильдии
        client_guild_name = guild['name']
        guild_id = func.guild_exist(client_guild_name, client_id)  # Поиск гильдии в БД
        players_ally = func.get_players(guild)  # Получаем список игроков гильдии
        players = func.get_players_info(players_ally)  # Получаем информацию о игроках гильдии
        for player in players:
            if func.user_exist(player):  # Если пользовать уже есть в БД
                old_roster = func.get_roster(player['allyCode'])  # Получаем список персонажей игрока из БД
                func.roster_updated(player, old_roster, guild_id)  # Сверяем персонажей
            else:
                func.add_user(player, guild_id)  # Добавляем игрока в БД
    print(f"Цикл завершён, следующий цикл через {interval} минут...")
    time.sleep(60*interval)
