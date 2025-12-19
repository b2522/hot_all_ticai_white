import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_current_time():
    """获取当前时间（时分，24小时制）"""
    now = datetime.datetime.now()
    return now.hour, now.minute

def is_valid_crawl_time():
    """检查是否在允许的抓取时间范围内（15:00到9:00）"""
    hour, minute = get_current_time()
    
    # 允许的时间范围：15:00到第二天9:00
    # 即hour >= 15 或者 hour < 9
    return hour >= 15 or hour < 9

# 检查当前时间
now = datetime.datetime.now()
hour, minute = get_current_time()
is_valid = is_valid_crawl_time()

logging.info(f"当前时间：{hour:02d}:{minute:02d}")
logging.info(f"是否在允许的抓取时间范围内：{is_valid}")
logging.info(f"允许的时间范围：15:00到第二天9:00")

# 测试几个不同的时间
test_times = [(8, 59), (9, 0), (14, 59), (15, 0), (23, 59), (0, 0)]

for test_hour, test_minute in test_times:
    # 模拟时间
    is_valid_test = test_hour >= 15 or test_hour < 9
    logging.info(f"测试时间 {test_hour:02d}:{test_minute:02d} - 是否允许：{is_valid_test}")
