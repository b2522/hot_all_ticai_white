import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = "stock_data.db"

def check_stock_data():
    """检查数据库中的股票数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # 检查表中的数据量
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            logging.info(f"表 {table_name} 中共有 {count} 条数据")
            
            # 如果是20251201表，显示前5条数据
            if table_name == "stock_20251201":
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                rows = cursor.fetchall()
                logging.info(f"表 {table_name} 的前5条数据:")
                for row in rows:
                    logging.info(row)
                    
    except Exception as e:
        logging.error(f"检查数据失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # 检查当前数据库中的股票数据
    check_stock_data()
