import os

import pymysql
import yaml
from botpy import logging
from pymysql import MySQLError

_log = logging.get_logger()


class Mapper:
    def __init__(self):
        _log.info("[Controller] 初始化机器人配置信息")
        ## 读取配置文件
        with open(os.path.join(os.getcwd(), "config", "mysql.yml"), 'r') as file:
            config: dict = yaml.safe_load(file)
            _log.info(f"[Controller] 机器人配置文件: {config}")
        self.cfg: dict = config["database"]

    def get_conn(self):
        return pymysql.connect(
            user=self.cfg["username"],
            port=self.cfg["port"],
            password=self.cfg["password"],
            host=self.cfg["host"],
            database=self.cfg["database"],
        )

    # MYSQL 修改数据函数
    def execute_update_query(self, query, params):
        connection = None
        success = False
        try:
            # 连接到 MySQL 数据库
            connection = self.get_conn()

            with connection.cursor() as cursor:
                # 如果有提供 params 参数，执行更新语句时会用 params 替代 query 中的占位符
                cursor.execute(query, params)
                connection.commit()  # 提交事务

                # 如果执行影响的行数大于0，表示更新成功
                if cursor.rowcount > 0:
                    success = True
                else:
                    success = False

        except MySQLError as e:
            print(f"数据库错误类型: {type(e)}")
            print(f"数据库错误信息: {e}")
            success = False
        except Exception as e:
            print(f"其他错误类型: {type(e)}")
            print(f"错误信息: {e}")
            success = False
        finally:
            # 确保连接关闭
            if connection:
                connection.close()

        return success

    def execute_insert_query(self, query, params):
        connection = None
        inserted_id = None  # 初始化插入的 ID 为 None
        success = False

        try:
            # 连接到 MySQL 数据库
            connection = self.get_conn()

            with connection.cursor() as cursor:
                cursor.execute(query, params)  # 执行插入语句，params 用来传递 SQL 参数
                connection.commit()  # 提交事务

                # 如果执行影响的行数大于0，表示插入成功
                if cursor.rowcount > 0:
                    success = True
                    inserted_id = cursor.lastrowid  # 获取最后插入记录的 ID
                else:
                    success = False

        except MySQLError as e:
            print(f"数据库错误类型: {type(e)}")
            print(f"数据库错误信息: {e}")
            success = False
        except Exception as e:
            print(f"其他错误类型: {type(e)}")
            print(f"错误信息: {e}")
            success = False
        finally:
            # 确保连接关闭
            if connection:
                connection.close()

        # 返回插入结果（ID 或 False）
        if success:
            return inserted_id  # 返回插入数据的 ID
        else:
            return None  # 如果插入失败，返回 None

    # MYSQL 语句查询函数
    def execute_sql_query(self, query, params):
        connection = None  # 初始化 connection 为 None
        try:
            # 连接到 MySQL 数据库
            connection = self.get_conn()

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # 返回字典形式的结果
                cursor.execute(query, params)

                # 获取所有查询结果
                result = cursor.fetchall()

                return result  # 返回查询结果，以字典的形式
        except Exception as e:
            print(f"错误类型: {type(e)}")
            print(f"错误信息: {e}")
            return None
        finally:
            # 确保连接已关闭（只有连接成功后才会关闭）
            if connection:
                connection.close()
