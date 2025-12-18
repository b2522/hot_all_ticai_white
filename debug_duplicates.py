import sqlite3
from db import search_stocks_by_keyword

# 搜索新能源股票
print("正在搜索'新能源'股票...")
results = search_stocks_by_keyword('新能源')

# 找出所有龙洲股份的记录
longzhou_stocks = [stock for stock in results if stock['name'] == '龙洲股份']

print(f"共找到 {len(longzhou_stocks)} 条龙洲股份的记录")

# 打印这些记录的详细信息
for i, stock in enumerate(longzhou_stocks):
    print(f"\n第 {i+1} 条记录:")
    print(f"  股票代码: {stock['code']}")
    print(f"  日期: {stock['date']}")
    print(f"  题材: {stock['plates']}")
    print(f"  描述: {stock['description']}")
    print(f"  涨停天数: {stock['m_days_n_boards']}")

# 查看这些记录来自哪些表
print("\n\n检查这些记录在数据库中的来源：")
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# 获取所有股票表
table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC"
cursor.execute(table_query)
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    print(f"\n表: {table_name}")
    
    # 查询龙洲股份的记录
    cursor.execute(f"SELECT code, date, plates FROM {table_name} WHERE name='龙洲股份'")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"  代码: {row[0]}, 日期: {row[1]}, 题材: {row[2]}")

# 关闭数据库连接
conn.close()
