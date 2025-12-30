import datetime
import db

# 获取今天的日期字符串
today = datetime.datetime.now()
today_str = today.strftime("%Y%m%d")

# 检查今天的数据是否存在
if db.date_has_data(today_str):
    print(f"表 stock_{today_str} 存在")
    
    # 获取今天的数据
    stocks = db.get_stock_data_by_date(today_str)
    print(f"表 stock_{today_str} 中有 {len(stocks)} 条数据")
    
    # 输出前5条数据作为样本
    print("\n数据样本（前5条）:")
    for stock in stocks[:5]:
        print(f"代码: {stock['code']}, 名称: {stock['name']}, 日期: {stock['date']}")
    
    # 检查今天的日期是否在可用日期列表中
    available_dates = db.get_available_dates()
    print(f"\n数据库中有数据的日期列表（共 {len(available_dates)} 个）:")
    print(available_dates)
    
    if today_str in available_dates:
        print(f"\n{today_str} 日期存在于可用日期列表中")
    else:
        print(f"\n{today_str} 日期不存在于可用日期列表中")
else:
    print(f"表 stock_{today_str} 不存在")