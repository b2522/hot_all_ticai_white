import sqlite3
from db import sort_stocks_by_plates

# 连接数据库
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# 获取所有股票表
table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'stock_%' ORDER BY name DESC"
cursor.execute(table_query)
tables = cursor.fetchall()

# 统计所有股票表中的题材出现总次数
print("正在统计所有表中的题材总出现次数...")
all_plate_counts = {}
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT plates FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        plates = row[0]
        if plates:
            plate_list = plates.split('、')
            for plate in plate_list:
                all_plate_counts[plate] = all_plate_counts.get(plate, 0) + 1

print(f"共统计了 {len(all_plate_counts)} 个不同题材")
print("\n各题材出现总次数：")
sorted_plates = sorted(all_plate_counts.items(), key=lambda x: x[1], reverse=True)
for i, (plate, count) in enumerate(sorted_plates[:10]):
    print(f"{i+1}. {plate}: {count}次")
print("...")

# 对每个表的数据进行排序测试
for table in tables:
    table_name = table[0]
    print(f"\n\n=== 测试表：{table_name} ===")
    
    # 获取表中的所有数据
    cursor.execute(f"SELECT code, name, plates FROM {table_name}")
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
    
    print(f"表中共有 {len(stocks)} 条股票记录")
    
    # 应用排序
    sorted_stocks = sort_stocks_by_plates(stocks)
    
    # 检查排序是否正确
    issues_found = False
    for i in range(len(sorted_stocks) - 1):
        current = sorted_stocks[i]
        next_stock = sorted_stocks[i + 1]
        
        # 计算当前股票的排序键
        current_plates = current.get('plates', '')
        if current_plates:
            current_plate_list = current_plates.split('、')
            current_plate_count = len(current_plate_list)
            current_total = sum(all_plate_counts.get(plate, 0) for plate in current_plate_list)
        else:
            current_plate_count = 0
            current_total = 0
        
        # 计算下一个股票的排序键
        next_plates = next_stock.get('plates', '')
        if next_plates:
            next_plate_list = next_plates.split('、')
            next_plate_count = len(next_plate_list)
            next_total = sum(all_plate_counts.get(plate, 0) for plate in next_plate_list)
        else:
            next_plate_count = 0
            next_total = 0
        
        # 检查排序是否符合规则
        if current_plate_count > next_plate_count:
            # 当前股票题材数量多，排序正确
            pass
        elif current_plate_count < next_plate_count:
            # 当前股票题材数量少，排序错误
            print(f"排序错误: {current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
            print(f"应该排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 后面")
            issues_found = True
        else:
            # 题材数量相同，检查总出现次数
            if current_total > next_total:
                # 当前股票总出现次数多，排序正确
                pass
            elif current_total < next_total:
                # 当前股票总出现次数少，排序错误
                print(f"排序错误: {current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
                print(f"应该排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 后面")
                issues_found = True
            else:
                # 总出现次数也相同，检查题材具体内容
                current_plate_total = sum(all_plate_counts.get(plate, 0) for plate in current_plate_list)
                next_plate_total = sum(all_plate_counts.get(plate, 0) for plate in next_plate_list)
                if current_plate_total != next_plate_total:
                    print(f"总出现次数计算异常: {current['name']} vs {next_stock['name']}")
                    print(f"  当前股票题材: {current_plates}")
                    print(f"  下一个股票题材: {next_plates}")
                    issues_found = True
    
    if not issues_found:
        print(f"表 {table_name} 的排序完全正确！")
    else:
        print(f"表 {table_name} 共发现 {issues_found} 个排序问题")

# 测试搜索功能的排序
print("\n\n=== 测试搜索功能的排序 ===")
from db import search_stocks_by_keyword

# 测试不同关键词
keywords = ['液冷', '光通信', '人工智能', '新能源', '半导体']

for keyword in keywords:
    print(f"\n搜索关键词: '{keyword}'")
    results = search_stocks_by_keyword(keyword)
    print(f"搜索结果数量: {len(results)}")
    
    # 检查搜索结果的排序
    search_issues_found = False
    for i in range(len(results) - 1):
        current = results[i]
        next_stock = results[i + 1]
        
        # 计算当前股票的排序键
        current_plates = current.get('plates', '')
        if current_plates:
            current_plate_list = current_plates.split('、')
            current_plate_count = len(current_plate_list)
            current_total = sum(all_plate_counts.get(plate, 0) for plate in current_plate_list)
        else:
            current_plate_count = 0
            current_total = 0
        
        # 计算下一个股票的排序键
        next_plates = next_stock.get('plates', '')
        if next_plates:
            next_plate_list = next_plates.split('、')
            next_plate_count = len(next_plate_list)
            next_total = sum(all_plate_counts.get(plate, 0) for plate in next_plate_list)
        else:
            next_plate_count = 0
            next_total = 0
        
        # 检查排序是否符合规则
        if current_plate_count > next_plate_count:
            # 当前股票题材数量多，排序正确
            pass
        elif current_plate_count < next_plate_count:
            # 当前股票题材数量少，排序错误
            print(f"  搜索结果排序错误: {current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
            print(f"  应该排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 后面")
            search_issues_found = True
        else:
            # 题材数量相同，检查总出现次数
            if current_total > next_total:
                # 当前股票总出现次数多，排序正确
                pass
            elif current_total < next_total:
                # 当前股票总出现次数少，排序错误
                print(f"  搜索结果排序错误: {current['name']} (题材数量: {current_plate_count}, 总出现次数: {current_total})")
                print(f"  应该排在 {next_stock['name']} (题材数量: {next_plate_count}, 总出现次数: {next_total}) 后面")
                search_issues_found = True
    
    if not search_issues_found and len(results) > 0:
        print("  搜索结果排序完全正确！")
    
    # 显示前几条结果
    if len(results) > 0:
        print("  搜索结果前3条：")
        for i, stock in enumerate(results[:3]):
            plates = stock.get('plates', '')
            plate_count = len(plates.split('、')) if plates else 0
            if plates:
                plate_list = plates.split('、')
                total_occurrences = sum(all_plate_counts.get(plate, 0) for plate in plate_list)
            else:
                total_occurrences = 0
            print(f"    {i+1}. {stock['name']} (题材数量: {plate_count}, 总出现次数: {total_occurrences})")

# 关闭数据库连接
conn.close()
print("\n\n=== 测试完成 ===")
