import sqlite3
import os

# 数据库文件路径
DB_PATH = "stock_data.db"

def check_stock_records(stock_name):
    """检查指定股票名称在所有日期的记录"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        print(f"检查股票 '{stock_name}' 的记录:")
        print(f"共找到 {len(tables)} 个股票数据表")
        print("-" * 60)
        
        found_in_any_table = False
        
        # 遍历所有表，搜索指定股票名称
        for table in tables:
            table_name = table[0]
            date_str = table_name.replace('stock_', '')
            
            # 构建搜索SQL
            search_sql = f"""
            SELECT DISTINCT code, name, description, plates, m_days_n_boards, date 
            FROM {table_name} 
            WHERE name = ?
            """
            
            # 执行搜索
            cursor.execute(search_sql, (stock_name,))
            rows = cursor.fetchall()
            
            if rows:
                found_in_any_table = True
                print(f"日期 {date_str} 包含 {len(rows)} 条 '{stock_name}' 的记录")
                for row in rows:
                    print(f"  - {row[1]} ({row[0]}): {row[4]}, {row[3]}")
            else:
                print(f"日期 {date_str} 没有找到 '{stock_name}' 的记录")
        
        print("-" * 60)
        if not found_in_any_table:
            print(f"未找到任何日期包含 '{stock_name}' 的记录")
            
    except Exception as e:
        print(f"查询数据库失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # 检查龙洲股份的记录
    check_stock_records("龙洲股份")
