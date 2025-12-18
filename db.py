import sqlite3
import os
import logging
from pypinyin import lazy_pinyin, Style

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 数据库文件路径
DB_PATH = "stock_data.db"

def init_db():
    """初始化数据库"""
    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 创建表的函数（会在存储数据时调用）
        logging.info("数据库初始化完成")
        
    except Exception as e:
        logging.error(f"数据库初始化失败: {e}")
    finally:
        conn.close()

def create_table(date_str):
    """为指定日期创建股票数据表"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 表名使用日期，例如：stock_20251201
        table_name = f"stock_{date_str}"
        
        # 创建表结构
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            plates TEXT,
            m_days_n_boards TEXT,
            date TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        logging.info(f"成功创建表: {table_name}")
        
    except Exception as e:
        logging.error(f"创建表失败: {e}")
    finally:
        conn.close()

def store_stock_data(date_str, stock_data):
    """将股票数据存储到数据库（去重）"""
    # 创建表
    create_table(date_str)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        table_name = f"stock_{date_str}"
        
        # 首先创建唯一索引来防止重复
        try:
            cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS idx_{table_name}_code ON {table_name}(code)")
        except Exception as e:
            logging.warning(f"创建唯一索引失败: {e}")
        
        # 使用INSERT OR REPLACE来插入数据，如果有重复则替换
        insert_sql = f'''
        INSERT OR REPLACE INTO {table_name} (code, name, description, plates, m_days_n_boards, date)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        # 准备数据
        data_to_insert = []
        for stock in stock_data:
            data_to_insert.append((
                stock["code"],
                stock["name"],
                stock["description"],
                stock["plates"],
                stock["m_days_n_boards"],
                stock["date"]
            ))
        
        # 执行批量插入
        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()
        
        logging.info(f"成功将{len(data_to_insert)}条数据插入表{table_name}（已去重）")
        
    except Exception as e:
        logging.error(f"存储数据失败: {e}")
    finally:
        conn.close()

def get_all_stock_data():
    """获取所有日期的股票数据，按日期降序排列（去重）"""
    stock_dict = {}  # 使用字典去重，键为 code+date
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 遍历所有表，获取数据
        for table in tables:
            table_name = table[0]
            
            # 获取表中的所有数据
            cursor.execute(f"SELECT DISTINCT code, name, description, plates, m_days_n_boards, date FROM {table_name}")
            rows = cursor.fetchall()
            
            # 转换为字典格式
            for row in rows:
                code = row[0]
                date = row[5]
                unique_key = f"{code}_{date}"
                
                # 如果已经存在相同的键，跳过
                if unique_key in stock_dict:
                    continue
                
                code_part = code
                market = ""
                
                # 分割股票代码和市场
                if "." in code:
                    code_part, market = code.split(".")
                
                # 添加到字典中
                stock_dict[unique_key] = {
                    "code": code,
                    "code_part": code_part,
                    "market": market,
                    "name": row[1],
                    "description": row[2],
                    "plates": row[3],
                    "m_days_n_boards": row[4],
                    "date": date
                }
        
        # 转换为列表
        all_stocks = list(stock_dict.values())
        logging.info(f"成功获取{len(all_stocks)}条去重后的股票数据")
        
    except Exception as e:
        logging.error(f"获取数据失败: {e}")
    finally:
        conn.close()
    
    return all_stocks

def get_stock_data_by_date(date_str):
    """获取指定日期的股票数据"""
    stocks = []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        table_name = f"stock_{date_str}"
        
        # 检查表是否存在
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone():
            # 获取表中的所有数据
            cursor.execute(f"SELECT code, name, description, plates, m_days_n_boards, date FROM {table_name}")
            rows = cursor.fetchall()
            
            # 转换为字典格式
            for row in rows:
                code = row[0]
                code_part = code
                market = ""
                
                # 分割股票代码和市场
                if "." in code:
                    code_part, market = code.split(".")
                
                stocks.append({
                    "code": code,
                    "code_part": code_part,
                    "market": market,
                    "name": row[1],
                    "description": row[2],
                    "plates": row[3],
                    "m_days_n_boards": row[4],
                    "date": row[5]
                })
        
        # 应用新的排序规则：按照题材数量和同一题材股票数量排序
        sorted_stocks = sort_stocks_by_plates(stocks)
        
        logging.info(f"成功获取{date_str}的{len(sorted_stocks)}条股票数据，并完成排序")
        
    except Exception as e:
        logging.error(f"获取{date_str}的数据失败: {e}")
        sorted_stocks = []
    finally:
        conn.close()
    
    return sorted_stocks

def get_all_stock_names_and_codes():
    """获取所有股票名称和代码，用于搜索提示"""
    stock_info = set()  # 使用set避免重复，存储(name, code)元组
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        # 遍历所有表，获取股票名称和代码
        for table in tables:
            table_name = table[0]
            
            # 获取表中的所有股票名称和代码
            cursor.execute(f"SELECT DISTINCT name, code FROM {table_name}")
            data = cursor.fetchall()
            
            # 将股票名称和代码添加到set中
            for item in data:
                stock_info.add((item[0], item[1]))
        
        logging.info(f"成功获取{len(stock_info)}个不重复的股票名称和代码")
        
    except Exception as e:
        logging.error(f"获取股票名称和代码失败: {e}")
    finally:
        conn.close()
    
    return list(stock_info)

def date_has_data(date_str):
    """检查指定日期是否已有数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 检查对应的表是否存在
        table_name = f"stock_{date_str}"
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        
        if cursor.fetchone():
            # 检查表中是否有数据（超过2条视为有数据）
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            return count > 2
        return False
        
    except Exception as e:
        logging.error(f"检查日期{date_str}是否有数据失败: {e}")
        return False
    finally:
        conn.close()

def get_available_dates():
    """获取所有有数据的日期列表"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        available_dates = []
        for table in tables:
            table_name = table[0]
            # 从表名中提取日期部分，格式为YYYYMMDD
            date_str = table_name.replace('stock_', '')
            
            # 检查表中是否有数据
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            
            if count > 0:
                available_dates.append(date_str)
        
        logging.info(f"成功获取{len(available_dates)}个有数据的日期")
        return available_dates
        
    except Exception as e:
        logging.error(f"获取有数据的日期列表失败: {e}")
        return []
    finally:
        conn.close()

def sort_stocks_by_plates(stocks):
    """按照题材数量和同一题材股票数量对股票数据进行排序
    1. 题材数量多的股票排在前面
    2. 同一题材股票数量多的排在前面
    """
    if not stocks:
        return []
    
    # 首先获取所有股票数据来统计题材出现次数
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 统计每个题材出现的总次数（基于所有股票）
    plate_counts = {}
    
    try:
        # 获取所有股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%'")
        tables = cursor.fetchall()
        
        # 遍历所有表，统计题材出现次数
        for table in tables:
            table_name = table[0]
            
            # 查询表中的所有数据
            cursor.execute(f"SELECT plates FROM {table_name}")
            rows = cursor.fetchall()
            
            # 统计每个题材的出现次数
            for row in rows:
                plates = row[0]
                if plates:
                    plate_list = plates.split('、')
                    for plate in plate_list:
                        plate_counts[plate] = plate_counts.get(plate, 0) + 1
    finally:
        conn.close()
    
    # 创建一个列表，包含股票和它们的排序键
    stocks_with_keys = []
    for stock in stocks:
        plates = stock.get('plates', '')
        if plates:
            # 计算题材数量
            plate_list = plates.split('、')
            plate_count = len(plate_list)
            
            # 计算该股票所属题材的总出现次数
            total_plate_occurrences = sum(plate_counts.get(plate, 0) for plate in plate_list)
        else:
            # 没有题材的股票排在最后
            plate_count = 0
            total_plate_occurrences = 0
        
        # 存储股票和排序键
        stocks_with_keys.append((
            stock,  # 股票数据
            (-plate_count, -total_plate_occurrences)  # 排序键
        ))
    
    # 排序
    stocks_with_keys.sort(key=lambda x: x[1])
    
    # 提取排序后的股票
    sorted_stocks = [stock for stock, key in stocks_with_keys]
    
    return sorted_stocks

def get_latest_day_data():
    """获取最新一天的数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取最新的股票表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
        latest_table = cursor.fetchone()
        
        if not latest_table:
            logging.info("没有找到最新的股票表")
            return []
        
        table_name = latest_table[0]
        
        # 获取最新一天的数据
        cursor.execute(f"SELECT DISTINCT code, name, description, plates, m_days_n_boards, date FROM {table_name}")
        rows = cursor.fetchall()
        
        # 转换为字典格式
        stocks = []
        for row in rows:
            code = row[0]
            code_part = code
            market = ""
            
            # 分割股票代码和市场
            if "." in code:
                code_part, market = code.split(".")
            
            stocks.append({
                "code": code,
                "code_part": code_part,
                "market": market,
                "name": row[1],
                "description": row[2],
                "plates": row[3],
                "m_days_n_boards": row[4],
                "date": row[5]
            })
        
        # 按照题材数量和同一题材股票数量排序
        sorted_stocks = sort_stocks_by_plates(stocks)
        
        logging.info(f"成功获取最新一天{table_name.replace('stock_', '')}的{len(sorted_stocks)}条股票数据")
        return sorted_stocks
        
    except Exception as e:
        logging.error(f"获取最新一天的数据失败: {e}")
        return []
    finally:
        conn.close()

def search_stocks_by_keyword(keyword):
    """根据关键词搜索所有日期的股票数据，并按日期降序排列"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 搜索结果列表（包含所有符合条件的记录，不按股票代码去重）
        search_results = []
        
        # 遍历所有表，搜索符合条件的数据
        for table in tables:
            table_name = table[0]
            
            # 构建搜索SQL，增加对code字段的搜索
            search_sql = f"""
            SELECT DISTINCT code, name, description, plates, m_days_n_boards, date 
            FROM {table_name} 
            WHERE name LIKE ? OR description LIKE ? OR plates LIKE ? OR code LIKE ?
            """
            
            # 执行搜索
            cursor.execute(search_sql, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
            rows = cursor.fetchall()
            
            # 转换为字典格式
            for row in rows:
                code = row[0]
                
                code_part = code
                market = ""
                
                # 分割股票代码和市场
                if "." in code:
                    code_part, market = code.split(".")
                
                search_results.append({
                    "code": code,
                    "code_part": code_part,
                    "market": market,
                    "name": row[1],
                    "description": row[2],
                    "plates": row[3],
                    "m_days_n_boards": row[4],
                    "date": row[5]
                })
        
        
        # 应用新的排序规则：按照题材数量和同一题材股票数量排序
        sorted_results = sort_stocks_by_plates(search_results)
        
        logging.info(f"成功搜索到{len(search_results)}条去重后的股票数据，并完成排序")
        
    except Exception as e:
        logging.error(f"搜索股票数据失败: {e}")
        sorted_results = []
    finally:
        conn.close()
    
    return sorted_results

def search_stocks_by_plate(plate):
    """根据题材搜索股票数据，支持模糊匹配和拼音搜索"""
    if not plate:
        return []
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 搜索结果列表
        search_results = []
        
        # 遍历所有表，搜索符合条件的数据
        for table in tables:
            table_name = table[0]
            
            # 构建搜索SQL，先获取所有数据
            search_sql = f"""
            SELECT DISTINCT code, name, description, plates, m_days_n_boards, date 
            FROM {table_name}
            """
            
            # 执行搜索
            cursor.execute(search_sql)
            rows = cursor.fetchall()
            
            # 转换为字典格式并进行拼音首字母筛选
            for row in rows:
                code = row[0]
                stock_plates = row[3]
                
                # 如果股票没有题材，跳过
                if not stock_plates:
                    continue
                
                # 检查是否直接包含查询关键词（不区分大小写）
                if plate.lower() in stock_plates.lower():
                    match = True
                    logging.info(f"直接匹配: {stock_plates} 包含 {plate}")
                else:
                    # 检查拼音首字母
                    match = False
                    plate_list = stock_plates.split('、')
                    
                    for current_plate in plate_list:
                        # 获取题材的拼音首字母
                        pinyin_initial = ''.join(lazy_pinyin(current_plate, style=Style.FIRST_LETTER))
                        
                        # 检查拼音首字母是否精确匹配查询关键词（不区分大小写）
                        if plate.lower() == pinyin_initial.lower():
                            match = True
                            logging.info(f"拼音首字母匹配: {current_plate} 的拼音首字母 {pinyin_initial} 匹配 {plate}")
                            break
                    if not match:
                        logging.info(f"未匹配: {stock_plates} 不包含 {plate}，拼音首字母也不匹配")
                
                if match:
                    code_part = code
                    market = ""
                    
                    # 分割股票代码和市场
                    if "." in code:
                        code_part, market = code.split(".")
                    
                    search_results.append({
                        "code": code,
                        "code_part": code_part,
                        "market": market,
                        "name": row[1],
                        "description": row[2],
                        "plates": stock_plates,
                        "m_days_n_boards": row[4],
                        "date": row[5]
                    })
        
        # 应用新的排序规则：按照题材数量和同一题材股票数量排序
        sorted_results = sort_stocks_by_plates(search_results)
        
        logging.info(f"成功搜索到{len(search_results)}条去重后的股票数据，并完成排序")
        
    except Exception as e:
        logging.error(f"搜索股票数据失败: {e}")
        sorted_results = []
    finally:
        conn.close()
    
    return sorted_results

def get_stock_history_data(stock_code):
    """根据股票代码获取该股票的历史上榜数据"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取所有股票表，并按日期降序排列
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC")
        tables = cursor.fetchall()
        
        # 历史数据列表
        history_data = []
        
        # 遍历所有表，获取该股票的数据
        for table in tables:
            table_name = table[0]
            
            # 构建查询SQL
            query_sql = f"""
            SELECT DISTINCT code, name, description, plates, m_days_n_boards, date 
            FROM {table_name} 
            WHERE code LIKE ?
            """
            
            # 执行查询
            cursor.execute(query_sql, (f"%{stock_code}%",))
            rows = cursor.fetchall()
            
            # 转换为字典格式
            for row in rows:
                code = row[0]
                
                code_part = code
                market = ""
                
                # 分割股票代码和市场
                if "." in code:
                    code_part, market = code.split(".")
                
                history_data.append({
                    "code": code,
                    "code_part": code_part,
                    "market": market,
                    "name": row[1],
                    "description": row[2],
                    "plates": row[3],
                    "m_days_n_boards": row[4],
                    "date": row[5]
                })
        
        logging.info(f"成功获取股票{stock_code}的{len(history_data)}条历史数据")
        
    except Exception as e:
        logging.error(f"获取股票历史数据失败: {e}")
        history_data = []
    finally:
        conn.close()
    
    return history_data