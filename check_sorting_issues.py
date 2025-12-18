import sqlite3

# 导入排序函数
from db import sort_stocks_by_plates

conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# 获取最新的股票表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC LIMIT 1")
latest_table = cursor.fetchone()

if latest_table:
    print(f"测试表名: {latest_table[0]}")
    
    # 获取表中的所有数据
    cursor.execute(f"SELECT code, name, plates FROM {latest_table[0]}")
    rows = cursor.fetchall()
    
    # 转换为字典格式
    stocks = []
    for row in rows:
        stock = {
            'code': row[0],
            'name': row[1],
            'plates': row[2]
        }
        stocks.append(stock)
    
    # 统计每个题材的出现总次数（基于所有股票）
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
    except Exception as e:
        print(f"统计题材出现次数失败: {e}")
    
    # 应用排序
    sorted_stocks = sort_stocks_by_plates(stocks)
    
    # 检查排序是否正确
    print(f"\n检查所有股票的排序是否正确:")
    issues_found = False
    
    for i in range(len(sorted_stocks) - 1):
        current = sorted_stocks[i]
        next_stock = sorted_stocks[i + 1]
        
        # 计算当前股票的排序键
        current_plates = current.get('plates', '')
        if current_plates:
            current_plate_list = current_plates.split('、')
            current_plate_count = len(current_plate_list)
            current_total = sum(plate_counts.get(plate, 0) for plate in current_plate_list)
        else:
            current_plate_count = 0
            current_total = 0
        
        # 计算下一个股票的排序键
        next_plates = next_stock.get('plates', '')
        if next_plates:
            next_plate_list = next_plates.split('、')
            next_plate_count = len(next_plate_list)
            next_total = sum(plate_counts.get(plate, 0) for plate in next_plate_list)
        else:
            next_plate_count = 0
            next_total = 0
        
        # 检查排序规则
        if current_plate_count < next_plate_count:
            # 当前股票题材数量少，排序错误
            print(f"\n排序错误 #{i+1}:")
            print(f"{current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
            print(f"排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 前面")
            print(f"但{current['name']}的题材数量更少")
            issues_found = True
        elif current_plate_count == next_plate_count:
            # 题材数量相同，检查总出现次数
            if current_total < next_total:
                # 当前股票总出现次数少，排序错误
                print(f"\n排序错误 #{i+1}:")
                print(f"{current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
                print(f"排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 前面")
                print(f"但{current['name']}的题材总出现次数更少")
                issues_found = True
    
    if issues_found:
        print(f"\n发现了 {issues_found} 个排序错误")
    else:
        print("\n所有股票的排序都符合规则！")
    
    # 检查具体案例 - 生益科技和生益电子
    print(f"\n检查具体案例:")
    for i, stock in enumerate(sorted_stocks):
        if stock['name'] in ['生益科技', '生益电子']:
            plates = stock.get('plates', '')
            plate_count = len(plates.split('、')) if plates else 0
            total_occurrences = sum(plate_counts.get(p, 0) for p in plates.split('、')) if plates else 0
            print(f"{i+1}. {stock['name']}: {plates} (题材数量: {plate_count}, 总出现次数: {total_occurrences})")
    
    # 检查所有题材数量相同的股票
    print(f"\n检查题材数量相同的股票组:")
    plate_count_groups = {}
    for stock in sorted_stocks:
        plates = stock.get('plates', '')
        plate_count = len(plates.split('、')) if plates else 0
        if plate_count not in plate_count_groups:
            plate_count_groups[plate_count] = []
        plate_count_groups[plate_count].append(stock)
    
    for count in sorted(plate_count_groups.keys(), reverse=True):
        stocks_in_group = plate_count_groups[count]
        print(f"\n题材数量为 {count} 的股票有 {len(stocks_in_group)} 个:")
        
        # 检查这个组内的排序是否正确
        for i in range(len(stocks_in_group) - 1):
            current = stocks_in_group[i]
            next_stock = stocks_in_group[i + 1]
            
            current_plates = current.get('plates', '')
            current_total = sum(plate_counts.get(p, 0) for p in current_plates.split('、')) if current_plates else 0
            
            next_plates = next_stock.get('plates', '')
            next_total = sum(plate_counts.get(p, 0) for p in next_plates.split('、')) if next_plates else 0
            
            if current_total < next_total:
                print(f"  排序错误: {current['name']} (总出现次数: {current_total}) 排在 {next_stock['name']} (总出现次数: {next_total}) 前面")
                issues_found = True
    
    if not issues_found:
        print("\n所有组内的排序都符合规则！")

else:
    print('没有找到股票表')

conn.close()