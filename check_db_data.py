#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库文件路径
DB_PATH = "stock_data.db"

def check_plate_data():
    """检查数据库中的题材数据格式"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
        latest_table = cursor.fetchone()
        
        if not latest_table:
            logging.error("没有找到股票表")
            return
        
        table_name = latest_table[0]
        logging.info(f"检查最新表: {table_name}")
        
        # 先查看表的结构
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        logging.info(f"表结构: {columns}")
        
        # 查询包含'消费'或拼音首字母'dxf'相关的股票
        search_sql = f"""
        SELECT DISTINCT code, name, description, plates, m_days_n_boards, date 
        FROM {table_name} 
        WHERE plates LIKE ?
        """
        
        # 搜索包含'大消费'或'消费'的股票
        cursor.execute(search_sql, ("%消费%",))
        rows = cursor.fetchall()
        
        logging.info(f"找到 {len(rows)} 条包含'消费'的股票数据")
        
        if rows:
            logging.info("前5条数据:")
            for row in rows[:5]:
                code = row[0]
                name = row[1]
                stock_plates = row[3]
                logging.info(f"股票: {code} - {name}")
                logging.info(f"题材: {stock_plates}")
                if stock_plates:
                    plate_list = stock_plates.split('、')
                    logging.info(f"分割后: {plate_list}")
                    logging.info("-")
        
        # 查看所有题材数据的格式
        logging.info("\n查看所有题材数据的格式样本:")
        cursor.execute(f"SELECT DISTINCT plates FROM {table_name} WHERE plates IS NOT NULL AND plates != '' LIMIT 20")
        plate_samples = cursor.fetchall()
        
        for i, sample in enumerate(plate_samples):
            stock_plates = sample[0]
            logging.info(f"样本 {i+1}: {stock_plates}")
            if stock_plates:
                plate_list = stock_plates.split('、')
                logging.info(f"   分割后: {plate_list}")
                logging.info(f"   数量: {len(plate_list)}")
        
    except Exception as e:
        logging.error(f"检查数据库数据失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_plate_data()
