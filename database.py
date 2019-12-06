import pymysql
# 打开数据库连接
# db = pymysql.connect("localhost", "root", "flamer", "mydb")
# 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT * FROM mydb.data_event")
# 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
# print(data)
# 关闭数据库连接
# db.close()


def Insert(db, table, data):
    sql = "INSERT INTO %s VALUES%s"%(pymysql.escape_string(table), str(data))
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def Search(cursor, table, key=1, key_word=1, output=False):
    # 输入游标对象cursor，查询表格，查询信息类别和查询内容，返回包含该内容的所有数据，output为True时还将输出列名元组
    sql = "SELECT * FROM %s WHERE %s like '%s'"%(pymysql.escape_string(table), key, key_word)
    cursor.execute(sql)
    col = cursor.description
    data = cursor.fetchall()
    if output == 0:
        return data
    else:
        return data, col


def Show_street_events(cursor, time, type):
    # 输入游标对象cursor，查询时间和色块分类依据（大类/小类名称），返回一个二维字典
    datas, name_of_col = Search(cursor, "mydb.data_event", "CREATE_TIME", time+"%", True)
    number_of_event = {}
    street = 15  # 街道名称列的下标
    type_value = -1
    for i in range(len(name_of_col)):
        if name_of_col[i][0] == type:
            type_value = i
            break
    if type_value == -1:
        return {}
    for data in datas:
        if data[street] in number_of_event:
            if data[type_value] in number_of_event[data[street]]:
                number_of_event[data[street]].update({data[type_value]:
                                                      number_of_event[data[street]][data[type_value]]+1})
            else:
                number_of_event[data[street]].update({data[type_value]: 1})
        else:
            number_of_event.update({data[street]: {data[type_value]: 1}})
    return number_of_event


def Show():
    a = 0


if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "flamer", "mydb")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    d = Show_street_events(cursor, '2018-02-08', 'SUB_TYPE_NAME')
    print(d)
    # user = ('2','727016587@qq.com','123','aab')
    # Insert(cursor, "mydb.users", user)
