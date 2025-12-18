#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import logging
import sys
import os

# 添加当前目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def examine_plate_data():
    """检查数据库中的题材字段内容"""
    logging.info("检查数据库中的题材字段内容")
    logging.info("=" * 50)
    
    try:
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
        latest_table = cursor.fetchone()
        
        if not latest_table:
            logging.info("没有找到股票表")
            return
        
        table_name = latest_table[0]
        logging.info(f"使用最新表: {table_name}")
        
        # 查询一些包含可疑题材的股票
        cursor.execute(f"""
        SELECT code, name, plates 
        FROM {table_name} 
        WHERE plates LIKE '%股权转让%' OR plates LIKE '%IP经济%'
        LIMIT 20
        """)
        
        rows = cursor.fetchall()
        
        logging.info(f"找到 {len(rows)} 条包含'股权转让'或'IP经济'的记录")
        logging.info("\n详细信息:")
        
        for row in rows:
            code, name, plates = row
            logging.info(f"股票: {code} - {name}")
            logging.info(f"题材: {plates}")
            
            # 检查是否包含'DXF'
            if 'DXF' in plates or 'dxf' in plates:
                logging.warning("⚠️  题材中包含'DXF'或'dxf'！")
            
            logging.info("-")
            
    except Exception as e:
        logging.error(f"查询数据库失败: {e}")
    finally:
        conn.close()
        
def test_dxf_in_plates():
    """测试'DXF'是否直接出现在任何题材字段中"""
    logging.info("\n" + "=" * 50)
    logging.info("测试'DXF'是否直接出现在任何题材字段中")
    
    try:
        conn = sqlite3.connect(db.DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
        latest_table = cursor.fetchone()
        
        if not latest_table:
            logging.info("没有找到股票表")
            return
        
        table_name = latest_table[0]
        
        # 直接查询包含'DXF'的记录
        cursor.execute(f"""
        SELECT code, name, plates 
        FROM {table_name} 
        WHERE plates LIKE '%DXF%' OR plates LIKE '%dxf%'
        """)
        
        rows = cursor.fetchall()
        
        logging.info(f"找到 {len(rows)} 条直接包含'DXF'或'dxf'的记录")
        
        for row in rows:
            code, name, plates = row
            logging.info(f"股票: {code} - {name}")
            logging.info(f"题材: {plates}")
            logging.info("-")
            
    except Exception as e:
        logging.error(f"查询数据库失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    examine_plate_data()
    test_dxf_in_plates()