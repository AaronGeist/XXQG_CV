# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:23:51 2021

@author: XTian
"""
#修改24-29之间的服务器信息
import sys
import socket
import pymysql.cursors
import re

def extract_file(keyword, file_text):
    '''提取内容'''
    #使用正则提取关键字后面的数字
    result = re.findall('({}[\s\S]*?答案：[ABCD])'.format(keyword), file_text)
    print(result)
    return result


def sql_connection():
    '''建立数据连接'''
    #使用pymysql指令连接数据库
    connection = pymysql.connect(host = socket.gethostbyname(''),      #要连接的数据库的IP地址
                                 user = '',           #登录的账户名，如果登录的是最高权限账户则为root
                                 password = '',     #对应的密码
                                 port = 3306,
                                 db = 'sys',    #要连接的数据库
                                 charset = 'utf8mb4',     #设置编码格式
                                 #返回到Python的结果，以什么方式存储，如Dict.Cursor是以字典的方式存储
                                 #如果不加这行数据是以元组方式返回
                                 cursorclass = pymysql.cursors.DictCursor
                                 )
    return connection

def get_text_from_sql(connection,keyword):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `words` where name like '%{}%' and name like '%{}%'".format(keyword[0],keyword[1])
            cursor.execute(sql)
        connection.commit()
        results = cursor.fetchall()
    finally:
        print('关闭连接！')
        connection.close()
    return results
            
def insert_text_to_sql(connection,search_result,keyword):
    '''创建表'''
    try:
        # 使用cursor()方法获取操作游标word
        with connection.cursor() as cursor:
            '''判断表是否存在，如果不存在创建表'''
            sql_show_table = 'SHOW TABLES'
            cursor.execute(sql_show_table)
            tables = cursor.fetchall()
            table_list = []
            for table in tables:
                for value in table.values():
                    table_list.append(value)

            if 'words' not in table_list:
                sql = '''create table words(
                         name varchar(256) not null,
                         number varchar(256)) engine=InnoDB DEFAULT CHARSET=utf8;
                      '''
                cursor.execute(sql)
                print('创建表成功')
#查询SELECT * FROM `words` where name like '中国%'

        # 插入数据
        # 从数据库链接中得到cursor的数据结构
        num = 0;
        print('开始插入数据')
        for i in search_result:
            with connection.cursor() as cursor:
                sql = " insert into words(name, number) VALUES (%s, %s)"
                answer=re.findall('{}、[\s\S]*? '.format(i[-1]),i)
                cursor.execute(sql,(i[:-4],i[-1]+answer[0][2:-1]))
            # 执行到这一行指令时才是真正改变了数据库，之前只是缓存在内存中
            connection.commit()
            num += 1;
            print('成功插入{}条数据'.format(num))
        print('数据插入完毕！')

    except:
        # 发生错误时回滚
        connection.rollback()
        print('错误！')

    finally:
        # 关闭连接
        print('关闭连接！')
        connection.close()


def main(keyword1,keyword2):

    connection = sql_connection() #获取数据连接
    keyword=[keyword1,keyword2]
    results=get_text_from_sql(connection,keyword) #最终结果插入数据库
    # for i in results:
    #     print(i['name'])
    #     print(i['number'][:])
    # print('{}{}'.format('共查询到',len(results)))
    return(results)
    

if __name__ == '__main__':
    main()