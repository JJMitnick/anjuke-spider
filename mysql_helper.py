# -*-coding:utf-8-*-
# @time: 2020/5/3 11:16
# @author: Mitnick
# @description: MySQL工具类

import pymysql.cursors
from pymysql.err import MySQLError

import settings


class MysqlHelper(object):
    def __init__(self, config=None):
        """
        配置数据连接:MYSQL_MASTER={'host':'','port':'','user':'','pwd':'','db':''}
        :param config:指定读取数据库连接配置名称
        :raise ValueError:
        """
        if config is None:
            cfg = settings.MYSQL_CONNECTION
        else:
            cfg = getattr(settings, config)

        self.host = cfg['host']
        self.port = cfg['port']
        self.user = cfg['user']
        self.pwd = cfg['pwd']
        self.db = cfg['db']

    def __get_connection(self):
        """
        获取mysql数据库连接
        :return: 数据库连接 :raise: MySQLError
        """
        try:
            return pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db=self.db,
                                   charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        except MySQLError as err:
            raise err

    def query(self, sql=None):
        """
        查询
        :param sql:查询语句
        :return:tuple
        :raise MySQLError
        """
        if not sql:
            raise ValueError('sql is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        except MySQLError as err:
            raise err
        finally:
            conn.close()

    def execute(self, sql=None):
        """
        执行sql语句，执行后提交
        :param sql:
        :return:
        :raise MySQLError
        """
        if not sql:
            raise ValueError('sql is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)

            return conn.commit()
        except MySQLError as err:
            raise err
        finally:
            conn.close()

    def execute_args(self, sql=None, args=None):
        """
        执行sql语句，执行后提交
        :param sql:
        :return:
        :raise MySQLError
        """
        if not sql:
            raise ValueError('sql is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)

            return conn.commit()
        except MySQLError as err:
            raise err
        finally:
            conn.close()

    def call_procedure(self, procedure_name=None, procedure_args=()):
        """
        调用存储过程,无输出参数
        :param procedure_name:
        :param procedure_args:如果是一个参数需要这样定义：(param,)
        :return:
        """
        if not procedure_name:
            raise ValueError('procedure_name is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procname=procedure_name, args=procedure_args)

            return conn.commit()
        except MySQLError as err:
            raise err
        finally:
            conn.close()

    def call_procedure_many(self, procedure_name=None, procedure_args_list=None):
        """
        批量添加数据
        :param procedure_name:
        :param procedure_args_list:
        :return:
        """
        if not procedure_name:
            raise ValueError('procedure_name is none')
        if not procedure_args_list:
            raise ValueError('procedure_args_list is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                for procedure_args in procedure_args_list:
                    try:
                        cursor.callproc(procname=procedure_name, args=procedure_args)
                    except MySQLError as err:
                        raise MySQLError('call error: %s data: %s' % (str(err), procedure_args))

            conn.commit()
        except MySQLError as err:
            raise err
        finally:
            conn.close()

    def call_procedure_out(self, procedure_name=None, procedure_args=(), out_param_count=1):
        """
        调用带输出参数的存储过程
        :param procedure_name:
        :param procedure_args:如果是一个参数需要这样定义：(param,)
        :param out_param_count:存储过程的输出参数个数
        :return:
        """
        if not procedure_name:
            raise ValueError('procedure_name is none')

        conn = self.__get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.callproc(procname=procedure_name, args=procedure_args)

            conn.commit()

            # 查询输出参数
            sql_out = "SELECT "
            for i in range(1, out_param_count + 1):
                sql_out += "@_{0}_{1}".format(procedure_name, str(i)) + ","
            # 去最后一个逗号
            sql_out = sql_out[0:len(sql_out) - 1]

            with conn.cursor() as cursor:
                cursor.execute(sql_out)
                return cursor.fetchall()
        except MySQLError as err:
            raise err
        finally:
            conn.close()
