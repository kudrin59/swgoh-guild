import sqlite3


class BotDB:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cursor = self.con.cursor()

    def close(self):
        self.con.close()

    def user_exist(self, ally):
        res = self.cursor.execute("SELECT `allycode` FROM `players` WHERE `allycode` = ?", (ally,))
        return bool(len(res.fetchall()))

    def add_user(self, player_name, ally):
        self.cursor.execute("INSERT INTO `players` (`name`, `allycode`) VALUES (?, ?)", (player_name, ally))
        return self.con.commit()

    def del_user(self, ally):
        self.cursor.execute("DELETE FROM `players` WHERE `allycode` = ?", (ally,))
        return self.con.commit()

    def add_roster(self, ally, name, data):
        self.cursor.execute(
            "INSERT INTO `player_roster` (`allycode`, `name`, `rarity`, `gear`, `relic`, `zetas`, `omicrons`) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (ally, name, data[0], data[1], data[2], data[3], data[4]))
        return self.con.commit()

    def get_roster(self, ally):
        res = self.cursor.execute("SELECT * FROM `player_roster` WHERE `allycode` = ?", (ally,))
        return res.fetchall()

    def del_roster(self, ally, name):
        res = self.cursor.execute("DELETE FROM `player_roster` WHERE `allycode` = ? and `name` = ?", (ally, name))
        return res.fetchall()

    def add_history(self, ally, name, old, new):
        self.cursor.execute(
            "INSERT INTO `history` (`allycode`, `name`, `old_rarity`, `old_gear`, `old_relic`, `old_zetas`, `old_omicrons`, `new_rarity`, `new_gear`, `new_relic`, `new_zetas`, `new_omicrons`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ally, name, old[0], old[1], old[2], old[3], old[4], new[0], new[1], new[2], new[3], new[4]))
        return self.con.commit()
