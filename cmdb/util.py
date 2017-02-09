import pymysql


def SQL(sql):
    conn = pymysql.connect(host='172.17.0.13', port=3306, user='lotus', passwd='ching', db='cmdb', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    data = cur.fetchall()
    return data