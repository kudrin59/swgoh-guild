from db import BotDB
from swgoh_help import *

BotDB = BotDB('db.db')


class func:
    omicron_skills = []

    @staticmethod
    def con():
        date = open('swgoh_help.txt', 'r').readline().split(";")
        user_login = date[0]
        user_pass = date[1]
        auth = settings(user_login, user_pass)
        return swgoh_help(auth)

    @staticmethod
    def get_guild(guild):
        print('Получаем информацию о гильдии...')
        sw = func.con()
        payload = {}
        payload['allycodes'] = guild
        payload['language'] = "rus_ru"
        payload['enums'] = True
        data = sw.fetchGuilds(payload)
        return data[0]

    @staticmethod
    def get_players(guild):
        print('Получаем список игроков гильдии...')
        allys = []
        for player in guild['roster']:
            allys.append(player['allyCode'])
        return allys

    @staticmethod
    def get_players_info(allys):
        print('Получаем информацию о игроках гильдии...')
        sw = func.con()
        payload = {}
        payload['allycodes'] = allys
        payload['language'] = "rus_ru"
        payload['enums'] = True
        payload['project'] = {"name": 1,
                              "allyCode": 1,
                              "roster": 1,
                              "equipped": 0,
                              "mods": 0}
        return sw.fetchPlayers(payload)

    @staticmethod
    def get_skill_list():
        print('Получаем список скиллов...')
        sw = func.con()
        payload = {}
        payload['collection'] = "skillList"
        payload['language'] = "rus_ru"
        payload['enums'] = True
        payload['project'] = {"id": 1,
                              "abilityReference": 1,
                              "isZeta": 1,
                              'tierList': 1
                              }
        items = sw.fetchData(payload)
        skills = {}
        for skill in items:
            skills[skill['id']] = skill
            omicrons = [tl['recipeId'] for tl in skill['tierList'] if "OMICRON" in tl['recipeId']]
            skills[skill['id']]['isOmicron'] = True if omicrons else False

        omicron_skills = [skill for skill in skills if skills[skill]['isOmicron']]
        return omicron_skills

    @staticmethod
    def get_clients():
        return BotDB.get_users()

    @staticmethod
    def guild_exist(client_guild_name, client_id):
        guild_id = BotDB.get_guild(client_guild_name)
        if not bool(len(guild_id)):
            guild_id = func.add_guild(client_id, client_guild_name)
        return guild_id[0][0]

    @staticmethod
    def add_guild(client_id, client_guild_name):
        guild_id = BotDB.add_guild(client_id, client_guild_name)
        print(f"Гильдия {client_guild_name} добавлена в БД!")
        return guild_id

    @staticmethod
    def get_guild_bd(client_id, client_guild_name):
        return BotDB.get_guild(client_id, client_guild_name)

    @staticmethod
    def user_exist(player):
        return BotDB.player_exist(player['allyCode'])

    @staticmethod
    def get_roster(ally):
        return BotDB.get_roster(ally)

    @staticmethod
    def roster_updated(player, old_roster, guild_id):
        updating = False
        for unit_roster in player['roster']:
            unit_zetas, unit_omicrons = func.get_zetas(unit_roster)
            if unit_roster['relic']:
                unit_relic = unit_roster['relic']['currentTier']
            else:
                unit_relic = 0
            find = False
            need_update = False
            new = [unit_roster['rarity'], unit_roster['gear'], unit_relic, unit_zetas, unit_omicrons]
            old = []
            for unit_old_roster in old_roster:
                name = unit_old_roster[1]
                rarity = unit_old_roster[2]
                gear = unit_old_roster[3]
                relic = unit_old_roster[4]
                zetas = unit_old_roster[5]
                omicrons = unit_old_roster[6]
                old = [rarity, gear, relic, unit_zetas, unit_omicrons]
                if unit_roster['nameKey'] == name:
                    find = True
                    if unit_roster['rarity'] != rarity or unit_roster[
                        'gear'] != gear or unit_relic != relic or unit_zetas != zetas or unit_omicrons != omicrons:
                        need_update = True
                    break
            if find:
                if need_update:
                    BotDB.del_roster(player['allyCode'], unit_roster['nameKey'])
                    BotDB.add_roster(player['allyCode'], unit_roster['nameKey'], new)
                    BotDB.add_history(player['allyCode'], unit_roster['nameKey'], old, new)
                    updating = True
            else:
                BotDB.add_roster(player['allyCode'], unit_roster['nameKey'], new)
                updating = True
        if updating:
            BotDB.del_player(player['allyCode'])
            BotDB.add_player(player['name'], player['allyCode'], guild_id)
            print(f"Данные игрока {player['name']} обновлены!")

    @staticmethod
    def add_user(player, guild_id):
        BotDB.add_player(player['name'], player['allyCode'], guild_id)
        for unit in player['roster']:
            rarity = unit['rarity']
            gear = unit['gear']
            zetas, omicrons = func.get_zetas(unit)
            if unit['relic']:
                relic = unit['relic']['currentTier']
            else:
                relic = 0
            new = [rarity, gear, relic, zetas, omicrons]
            BotDB.add_roster(player['allyCode'], unit['nameKey'], new)
        print(f"Игрок {player['name']} добавлен в БД!")

    @staticmethod
    def get_zetas(unit):
        zetas = 0
        omicrons = 0
        for skill in unit['skills']:
            if skill['id'] in func.omicron_skills:
                if skill['isZeta']:
                    if skill['tier'] == skill['tiers']:
                        omicrons += 1
                        zetas += 1
                    elif skill['tier'] == skill['tiers'] - 1:
                        zetas += 1
                else:
                    if skill['tier'] == skill['tiers']:
                        omicrons += 1
            else:
                if skill['tier'] == skill['tiers'] and skill['isZeta']:
                    zetas += 1
        return zetas, omicrons
