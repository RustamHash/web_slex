import sqlite3
import time
import math
import re
from flask import url_for

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_user_by_login(self, login):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_contracts(self):
        sql = '''SELECT * FROM contracts'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Ошибка чтения из БД {e}")
        return []


    # def get_order(self, alias):
    #     try:
    #         self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if res:
    #             return res
    #     except sqlite3.Error as e:
    #         print("Ошибка получения статьи из БД "+str(e))
    #
    #     return (False, False)
    #
    # def get_order_body(self):
    #     try:
    #         self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
    #         res = self.__cur.fetchall()
    #         if res: return res
    #     except sqlite3.Error as e:
    #         print("Ошибка получения статьи из БД "+str(e))
    #
    #     return []
