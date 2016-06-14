# -*- coding:utf-8 -*- 
# author：zhouyang

import MySQLdb
import pandas as pd
from datetime import datetime
import numpy as np

con = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", db="ezlife", charset="utf8")
df = pd.read_csv("/Users/zhouyang/Downloads/20160613/sample.csv")

# 需要更换列名的列,及更换之后的列名对应关系
rename_dict = {
    "OD_or_amount": "od_or_amount",
    "Purification": "purification",
    "5_mod": "mod_5",
    "3_mod": "mod_3",
    "purchase_data": "purchase_date",
    "arrival_data": "arrival_date",
    "created_data": "create_date"
}
df = df.rename(columns=rename_dict)


# 将日期字符串转换为datetime数据类型
def transform_date(x):
    if len(x) != 14:
        print 'date is wrong. please check it later!'
        return np.nan
    year = int(x[:4])
    month = int(x[4:6])
    # 月份出现了0,非法!
    if month <= 0:
        month = 1
    day = int(x[6:8])
    # 日期出现了0,非法!
    if day <= 0:
        day = 1
    hour = int(x[8:10])
    min = int(x[10:12])
    second = int(x[12:])
    return datetime(year=year, month=month, day=day, hour=hour, minute=min, second=second)


# 需要将列purchaser移动到最后一列,然后删除末尾的 列:Unnamed: 19

columns = list(df)
columns = columns[:19]

df = df.ix[:, columns]
df['purchase_date'] = df['purchase_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))
df['arrival_date'] = df['arrival_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))
df['create_date'] = df['create_date'].map(lambda x: x if pd.isnull(x) else str(int(x)))

df['purchase_date'] = df['purchase_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))
df['arrival_date'] = df['arrival_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))
df['create_date'] = df['create_date'].map(lambda x: x if pd.isnull(x) else transform_date(x))


pd.io.sql.to_sql(df, 'sample', con, flavor='mysql', if_exists='append', index=False)