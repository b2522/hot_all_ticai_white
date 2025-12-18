import sqlite3
import os
from pypinyin import lazy_pinyin, FIRST_LETTER

DB_PATH = "stock_data.db"

def check_database_content():
    """检查数据库内容"""
    print("检查数据库内容...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        if not tables:
            print("数据库中没有股票表")
            return
            
        print(f"找到 {len(tables)} 个股票表:")
        for table in tables:
            table_name = table[0]
            
            # 获取表中的记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            # 获取表中的前5条记录
            cursor.execute(f"SELECT DISTINCT name, code FROM {table_name} LIMIT 5")
            sample_data = cursor.fetchall()
            
            print(f"  {table_name}: {count} 条记录")
            print(f"    示例数据: {sample_data}")
            
    except Exception as e:
        print(f"检查数据库内容失败: {e}")
    finally:
        conn.close()

def test_search_logic(keyword):
    """测试搜索逻辑"""
    print(f"\n测试搜索关键词: '{keyword}'")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        # 先测试直接数据库搜索
        print("\n直接数据库搜索结果:")
        all_db_results = set()
        for table in tables:
            table_name = table[0]
            
            # 搜索SQL
            search_sql = f"""
            SELECT DISTINCT name, code 
            FROM {table_name} 
            WHERE name LIKE ? OR description LIKE ? OR plates LIKE ? OR code LIKE ?
            """
            
            # 执行搜索
            cursor.execute(search_sql, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            rows = cursor.fetchall()
            
            for row in rows:
                all_db_results.add((row[0], row[1]))
        
        print(f"  数据库中匹配的股票数: {len(all_db_results)}")
        if len(all_db_results) <= 20:
            for name, code in sorted(all_db_results):
                print(f"    {name} ({code})")
        else:
            print(f"    显示前20个结果:")
            for name, code in sorted(list(all_db_results))[:20]:
                print(f"    {name} ({code})")
        
        # 测试app.py中的搜索逻辑
        print("\napp.py搜索逻辑结果:")
        stock_info = set()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT DISTINCT name, code FROM {table_name}")
            data = cursor.fetchall()
            for item in data:
                stock_info.add((item[0], item[1]))
        
        # 实现与app.py相同的搜索逻辑
        matched_results = []
        for name, code in stock_info:
            pinyin = ''.join(lazy_pinyin(name))
            pinyin_abbr = ''.join(lazy_pinyin(name, style=FIRST_LETTER))
            
            score = 0
            if keyword in name:
                score += 100
            if keyword.lower() in pinyin.lower():
                score += 50
            if keyword.lower() in pinyin_abbr.lower():
                score += 30
            if keyword in code:
                score += 80
            
            if score > 0:
                matched_results.append((name, score))
        
        matched_results.sort(key=lambda x: x[1], reverse=True)
        sorted_names = []
        seen_names = set()
        for name, score in matched_results:
            if name not in seen_names:
                seen_names.add(name)
                sorted_names.append(name)
        
        print(f"  app.py搜索结果数: {len(sorted_names)}")
        if len(sorted_names) <= 20:
            for name in sorted_names:
                print(f"    {name}")
        else:
            print(f"    显示前20个结果:")
            for name in sorted_names[:20]:
                print(f"    {name}")
        
        # 检查是否有遗漏
        app_names = set(sorted_names)
        db_names = {name for name, code in all_db_results}
        
        missing_in_app = db_names - app_names
        if missing_in_app:
            print(f"\n❌ app.py搜索遗漏的股票: {len(missing_in_app)}")
            for name in sorted(missing_in_app)[:20]:
                print(f"    {name}")
        else:
            print("\n✅ app.py搜索没有遗漏任何股票")
            
    except Exception as e:
        print(f"测试搜索逻辑失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # 检查数据库内容
    check_database_content()
    
    # 测试一些关键词
    keywords = ["科技", "华", "中", "贵州", "茅台"]
    
    for keyword in keywords:
        test_search_logic(keyword)
