import sqlite3

conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# 获取最新的股票表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
latest_table = cursor.fetchone()

if latest_table:
    print(f"最新表名: {latest_table[0]}")
    
    # 查询表中的数据
    cursor.execute(f"SELECT code, name, plates FROM {latest_table[0]} LIMIT 20")
    rows = cursor.fetchall()
    
    print('最新数据前20条：')
    for row in rows:
        print(row)
    
    # 查询一些有多个题材的股票
    cursor.execute(f"SELECT code, name, plates FROM {latest_table[0]} WHERE plates LIKE '%、%' LIMIT 10")
    multi_plate_stocks = cursor.fetchall()
    
    print('\n有多个题材的股票：')
    for row in multi_plate_stocks:
        print(row)
else:
    print('没有找到股票表')

conn.close()
