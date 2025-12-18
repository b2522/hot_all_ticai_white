#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
# 添加当前目录到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from pypinyin import lazy_pinyin, Style
import db  # 导入db模块以确保使用相同的环境

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def debug_pinyin():
    """调试拼音首字母问题"""
    logging.info("调试拼音首字母问题")
    logging.info("=" * 50)
    
    # 测试各种题材的拼音首字母
    test_plates = ["大消费", "大金融", "股权转让", "福建自贸", "航天", "AI医疗"]
    
    for plate in test_plates:
        # 直接调用lazy_pinyin
        pinyin = lazy_pinyin(plate)
        pinyin_initial = ''.join(lazy_pinyin(plate, style=Style.FIRST_LETTER))
        
        logging.info(f"题材: {plate}")
        logging.info(f"完整拼音: {pinyin}")
        logging.info(f"拼音首字母: {pinyin_initial}")
        
        # 检查匹配逻辑
        query = "DXF"  # 测试大消费的拼音首字母
        if plate == "大消费":
            match_exact = query.lower() == pinyin_initial.lower()
            match_startswith = pinyin_initial.lower().startswith(query.lower())
            logging.info(f"与'DXF'的精确匹配: {match_exact}")
            logging.info(f"与'DXF'的开头匹配: {match_startswith}")
            
            # 详细检查每个字符的拼音首字母
            for char in plate:
                char_pinyin = lazy_pinyin(char, style=Style.FIRST_LETTER)
                logging.info(f"字符 '{char}' 的拼音首字母: {char_pinyin}")
        
        logging.info("-")

if __name__ == "__main__":
    debug_pinyin()
