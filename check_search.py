import sqlite3
import sys
from pypinyin import lazy_pinyin, FIRST_LETTER

DB_PATH = "stock_data.db"

def check_stock_data():
    """检查数据库中的股票数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        print(f"共有{len(tables)}个股票数据表")
        
        # 统计每个表中的股票数量
        total_stocks = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_stocks += count
            print(f"  {table_name}: {count}条记录")
        
        print(f"\n数据库中共有{total_stocks}条股票记录")
        
        # 检查股票名称和代码的唯一性
        all_names_query = " UNION ALL ".join([f"SELECT name FROM {table[0]}" for table in tables])
        cursor.execute(f"SELECT COUNT(DISTINCT name) FROM ({all_names_query})")
        unique_names = cursor.fetchone()[0]
        
        all_codes_query = " UNION ALL ".join([f"SELECT code FROM {table[0]}" for table in tables])
        cursor.execute(f"SELECT COUNT(DISTINCT code) FROM ({all_codes_query})")
        unique_codes = cursor.fetchone()[0]
        
        print(f"\n不重复的股票名称: {unique_names}个")
        print(f"不重复的股票代码: {unique_codes}个")
        
        conn.close()
        
    except Exception as e:
        print(f"检查股票数据失败: {e}")

def test_search_function(keyword):
    """测试搜索功能"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 模拟后端搜索逻辑
        print(f"\n测试搜索关键词: '{keyword}'")
        
        # 1. 获取所有股票名称和代码
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        union_query = " UNION ALL ".join([f"SELECT DISTINCT name, code FROM {table[0]}" for table in tables])
        cursor.execute(f"SELECT DISTINCT name, code FROM ({union_query})")
        all_stock_info = cursor.fetchall()
        
        print(f"\n从数据库中获取了{len(all_stock_info)}个不重复的股票名称和代码")
        
        # 2. 模拟搜索逻辑
        matched_results = []
        for name, code in all_stock_info:
            # 转换为拼音首字母
            pinyin = ''.join(lazy_pinyin(name))
            # 转换为拼音首字母缩写
            pinyin_abbr = ''.join(lazy_pinyin(name, style=FIRST_LETTER))
            
            # 检查关键词是否在名称、拼音、拼音缩写或代码中
            if (keyword in name or 
                keyword.lower() in pinyin.lower() or 
                keyword.lower() in pinyin_abbr.lower() or 
                keyword in code):
                matched_results.append(name)
        
        # 去重
        matched_results = list(set(matched_results))
        print(f"\n搜索结果: {matched_results}")
        print(f"共找到{len(matched_results)}个匹配的股票名称")
        
        conn.close()
        
    except Exception as e:
        print(f"测试搜索功能失败: {e}")

if __name__ == "__main__":
    check_stock_data()
    if len(sys.argv) > 1:
        test_search_function(sys.argv[1])
    else:
        print("\n请提供搜索关键词作为参数，例如: python check_search.py 贵州茅台")
