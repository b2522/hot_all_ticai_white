import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库文件路径
DB_PATH = "stock_data.db"

def check_database():
    """检查数据库中的表和数据情况"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        if not tables:
            logging.info("数据库中没有股票表")
            return
        
        logging.info(f"数据库中共有{len(tables)}个股票表")
        
        # 检查每个表的数据量
        for table in tables:
            table_name = table[0]
            date_str = table_name.replace('stock_', '')
            
            # 检查数据量
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            # 检查第一条数据
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            first_row = cursor.fetchone()
            
            logging.info(f"表{table_name} (日期{date_str})：{count}条数据")
            if first_row:
                logging.info(f"  第一条数据：股票代码={first_row[1]}, 名称={first_row[2]}")
        
        # 检查最新的表是否有今天的数据
        today_table = tables[0][0]
        cursor.execute(f"SELECT * FROM {today_table} WHERE date = '{today_table.replace('stock_', '')}' LIMIT 1")
        today_data = cursor.fetchone()
        
        if today_data:
            logging.info(f"最新表{today_table}包含当天日期的数据")
        else:
            logging.warning(f"最新表{today_table}不包含当天日期的数据")
            
    except Exception as e:
        logging.error(f"检查数据库时出错: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_database()
