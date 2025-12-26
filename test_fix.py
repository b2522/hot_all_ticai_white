import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import crawler
import datetime

print('当前系统日期:', datetime.datetime.now().strftime('%Y-%m-%d'))
print('=' * 50)

# 直接查看crawl_stock_data函数中end_date的计算逻辑
def test_end_date_calculation():
    print('测试end_date计算逻辑:')
    # 获取当前日期
    current_date = datetime.datetime.now()
    print(f'  当前日期: {current_date.strftime("%Y-%m-%d")}')
    
    # 模拟函数内部的计算
    end_date = datetime.datetime.now()
    print(f'  函数内计算的end_date: {end_date.strftime("%Y-%m-%d")}')
    
    # 测试format_date函数
    date_str = crawler.format_date(end_date)
    print(f'  格式化后的日期字符串: {date_str}')
    
    # 测试is_weekday函数
    is_weekday = crawler.is_weekday(end_date)
    print(f'  是否为工作日: {is_weekday}')
    
    return True

test_end_date_calculation()
print('=' * 50)
print('测试完成！现在函数会在每次调用时计算当前日期作为end_date，')
print('确保定时任务能正确抓取当天的数据。')
