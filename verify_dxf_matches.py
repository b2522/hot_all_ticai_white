#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import os

# 添加当前目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("测试 DXF 搜索是否返回只包含 '股权转让' 或 'IP经济/谷子经济' 的股票")
logging.info("=" * 60)

# 1. 首先获取 DXF 搜索结果
logging.info("1. 获取 DXF 搜索结果:")
dxf_results = db.search_stocks_by_plate("DXF")
logging.info(f"找到 {len(dxf_results)} 条 DXF 搜索结果")

# 2. 筛选出只包含 '股权转让' 或 'IP经济/谷子经济' 的股票
logging.info("\n2. 筛选出可能的错误匹配:")
problematic_stocks = []

for stock in dxf_results:
    code = stock["code"]
    name = stock["name"]
    plates = stock["plates"]
    
    # Split the plates
    plate_list = plates.split('、')
    
    # Check if the stock has ONLY 股权转让 or ONLY IP经济/谷子经济
    has_dxf_plate = False
    has_problematic_plate = False
    
    for plate in plate_list:
        if "大消费" in plate:
            has_dxf_plate = True
        if "股权转让" in plate or "IP经济" in plate:
            has_problematic_plate = True
    
    # If it has problematic plates but no 大消费, it's a problem
    if has_problematic_plate and not has_dxf_plate:
        problematic_stocks.append(stock)

# 3. 显示问题股票
if problematic_stocks:
    logging.error(f"找到 {len(problematic_stocks)} 条错误匹配的股票:")
    for stock in problematic_stocks:
        logging.error(f"  代码: {stock['code']} | 名称: {stock['name']} | 题材: {stock['plates']}")
else:
    logging.info("✅ 没有找到错误匹配的股票")
    logging.info("这意味着所有匹配 'DXF' 的股票都包含 '大消费' 题材")
    logging.info("用户看到的 '股权转让' 和 'IP经济/谷子经济' 可能是因为这些股票同时包含 '大消费' 题材")

# 4. 显示一些实际的 DXF 搜索结果来验证
logging.info("\n3. 查看前 10 条 DXF 搜索结果的完整题材:")
for i, stock in enumerate(dxf_results[:10]):
    logging.info(f"[{i+1}] 代码: {stock['code']} | 名称: {stock['name']}")
    logging.info(f"    题材: {stock['plates']}")
    
    # 显示匹配的具体原因
    plate_list = stock['plates'].split('、')
    for plate in plate_list:
        from pypinyin import lazy_pinyin, Style
        pinyin_initial = ''.join(lazy_pinyin(plate, style=Style.FIRST_LETTER))
        if pinyin_initial.lower() == 'dxf':
            logging.info(f"    ✅ 匹配原因: '{plate}' 的拼音首字母是 '{pinyin_initial}'")
