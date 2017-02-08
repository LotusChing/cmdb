import MySQLdb


def SQL(sql):
    conn = MySQLdb.connect(host='192.168.2.20', port=3306, user='lotus', passwd='ching', db='cmdb', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    data = cur.fetchall()
    return data