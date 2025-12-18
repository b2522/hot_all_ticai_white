import sqlite3

# 连接数据库
db_path = "stock_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有股票表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
tables = cursor.fetchall()

if not tables:
    print("没有找到股票表")
    conn.close()
    exit()

# 使用最新的表
table_name = tables[0][0]
print(f"使用表: {table_name}")

# 查询包含问题题材的股票
print("\n查询包含 '股权转让'、'IP经济/谷子经济' 或 '大消费' 的股票:")
search_sql = f"SELECT code, plates FROM {table_name} WHERE plates LIKE ? OR plates LIKE ? OR plates LIKE ?"
cursor.execute(search_sql, ("%股权转让%", "%IP经济%", "%大消费%"))
rows = cursor.fetchall()

for code, plates in rows:
    print(f"\n股票代码: {code}")
    print(f"题材: {plates}")
    print(f"是否包含 'dxf': {'dxf' in plates.lower()}")
    print(f"是否包含 'dx': {'dx' in plates.lower()}")
    print(f"是否包含 'xf': {'xf' in plates.lower()}")

# 关闭数据库连接
conn.close()
