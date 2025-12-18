import sqlite3

DB_PATH = "stock_data.db"

def check_stock_names():
    """检查数据库中是否有包含特定关键词的股票名称"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        # 构建查询，查找包含"贵州"或"茅台"的股票名称
        if tables:
            union_query = " UNION ALL ".join([f"SELECT DISTINCT name, code FROM {table[0]}" for table in tables])
            # 先查看所有股票名称的前50个
            cursor.execute(f"SELECT DISTINCT name, code FROM ({union_query}) LIMIT 50")
            all_stocks = cursor.fetchall()
            
            print("数据库中前50个股票名称:")
            for name, code in all_stocks:
                print(f"  {name} ({code})")
            
            # 搜索包含"贵州"或"茅台"的股票
            cursor.execute(f"SELECT DISTINCT name, code FROM ({union_query}) WHERE name LIKE '%贵州%' OR name LIKE '%茅台%'")
            matched_stocks = cursor.fetchall()
            
            print(f"\n搜索到 {len(matched_stocks)} 个包含'贵州'或'茅台'的股票:")
            for name, code in matched_stocks:
                print(f"  {name} ({code})")
        
        conn.close()
        
    except Exception as e:
        print(f"查询数据库失败: {e}")

if __name__ == "__main__":
    check_stock_names()