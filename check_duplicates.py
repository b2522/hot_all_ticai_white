import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库文件路径
DB_PATH = "stock_data.db"

def check_duplicates():
    """检查数据库中的重复数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 遍历所有表，检查重复数据
        for table in tables:
            table_name = table[0]
            
            # 检查是否有重复的股票代码
            cursor.execute(f"SELECT code, COUNT(*) as count FROM {table_name} GROUP BY code HAVING count > 1")
            duplicates = cursor.fetchall()
            
            if duplicates:
                logging.warning(f"表{table_name}中有{len(duplicates)}个重复的股票代码:")
                for code, count in duplicates:
                    logging.warning(f"  - {code}: {count}次")
            else:
                logging.info(f"表{table_name}中没有重复的股票代码")
        
        # 检查跨表的重复数据
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        all_stocks = []
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT code, date FROM {table_name}")
            rows = cursor.fetchall()
            all_stocks.extend(rows)
        
        # 使用字典去重
        stock_dict = {}
        for stock in all_stocks:
            key = f"{stock[0]}_{stock[1]}"
            if key in stock_dict:
                stock_dict[key] += 1
            else:
                stock_dict[key] = 1
        
        # 检查是否有重复的股票-日期组合
        duplicate_count = sum(1 for count in stock_dict.values() if count > 1)
        if duplicate_count:
            logging.warning(f"跨表共有{duplicate_count}个重复的股票-日期组合")
        else:
            logging.info("跨表没有重复的股票-日期组合")
        
    except Exception as e:
        logging.error(f"检查重复数据失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_duplicates()
