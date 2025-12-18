import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库文件路径
DB_PATH = "stock_data.db"

def clean_duplicates():
    """清理数据库中的重复数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 遍历所有表，清理重复数据
        for table in tables:
            table_name = table[0]
            
            logging.info(f"开始清理表{table_name}中的重复数据")
            
            # 创建临时表，存储去重后的数据
            temp_table = f"temp_{table_name}"
            
            # 创建临时表
            cursor.execute(f'''
            CREATE TABLE {temp_table} AS 
            SELECT DISTINCT * FROM {table_name} 
            WHERE id IN (SELECT MIN(id) FROM {table_name} GROUP BY code)
            ''')
            
            # 删除原表
            cursor.execute(f"DROP TABLE {table_name}")
            
            # 重命名临时表为原表名
            cursor.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
            
            # 创建唯一索引
            try:
                cursor.execute(f"CREATE UNIQUE INDEX idx_{table_name}_code ON {table_name}(code)")
                logging.info(f"为表{table_name}创建唯一索引成功")
            except Exception as e:
                logging.warning(f"为表{table_name}创建唯一索引失败: {e}")
            
            # 提交更改
            conn.commit()
            
            logging.info(f"表{table_name}的重复数据清理完成")
        
        logging.info("所有表的重复数据清理完成")
        
    except Exception as e:
        logging.error(f"清理重复数据失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def recreate_db():
    """重新创建数据库，彻底清理所有数据"""
    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        # 删除所有股票表
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DROP TABLE {table_name}")
            logging.info(f"已删除表{table_name}")
        
        # 提交更改
        conn.commit()
        logging.info("所有股票表已删除，数据库已清理")
        
    except Exception as e:
        logging.error(f"重新创建数据库失败: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--recreate":
        # 彻底重新创建数据库
        recreate_db()
    else:
        # 仅清理重复数据
        clean_duplicates()
