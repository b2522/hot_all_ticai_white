import requests
import datetime
import db
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API基本URL
BASE_URL = "https://flash-api.xuangubao.com.cn/api/surge_stock/stocks"

# 开始日期：2025年12月1日
START_DATE = datetime.datetime(2025, 12, 1)
# 结束日期：今天
END_DATE = datetime.datetime.now()

def is_weekday(date):
    """判断日期是否为工作日（周一到周五）"""
    return date.weekday() < 5  # 0-4表示周一到周五

def format_date(date):
    """将日期格式化为YYYYMMDD格式"""
    return date.strftime("%Y%m%d")

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

def crawl_stock_data():
    """抓取从开始日期到今天的所有股票数据"""
    # 检查是否在允许的抓取时间范围内
    if not is_valid_crawl_time():
        logging.error("不在允许的抓取时间范围内（只能在15:00到9:00之间抓取）")
        return False
    
    current_date = START_DATE
    
    while current_date <= END_DATE:
        # 判断是否为工作日
        if is_weekday(current_date):
            date_str = format_date(current_date)
            
            # 检查该日期是否已有数据
            if db.date_has_data(date_str):
                logging.info(f"日期{date_str}已有数据，跳过抓取")
            else:
                logging.info(f"开始抓取{date_str}的股票数据")
                
                # 构建API URL
                url = f"{BASE_URL}?date={date_str}&normal=true&uplimit=true"
                
                try:
                    # 发送API请求
                    response = requests.get(url)
                    response.raise_for_status()  # 检查请求是否成功
                    
                    # 解析JSON数据
                    data = response.json()
                    
                    if data.get("code") == 20000 and data.get("data"):
                        # 获取股票数据项
                        items = data["data"].get("items", [])
                        
                        if items:
                            logging.info(f"成功获取{date_str}的{len(items)}条股票数据")
                            # 处理并存储数据
                            process_and_store_data(date_str, items)
                        else:
                            logging.info(f"{date_str}没有股票数据")
                    else:
                        logging.error(f"API返回错误: {data.get('message', '未知错误')}")
                        
                except requests.exceptions.RequestException as e:
                    logging.error(f"请求API失败: {e}")
                except Exception as e:
                    logging.error(f"处理数据时出错: {e}")
        else:
            date_str = format_date(current_date)
            logging.info(f"{date_str}是周末，跳过抓取")
        
        # 日期加1天（无论是否处理了当前日期，都会递增）
        current_date += datetime.timedelta(days=1)

def process_and_store_data(date_str, items):
    """处理股票数据并存储到数据库"""
    processed_data = []
    
    for item in items:
        try:
            # 提取需要的数据字段
            code = item[0]  # 股票代码
            name = item[1]  # 股票名称
            description = item[5]  # 解读
            
            # 处理所属题材，可能有多个值，用顿号隔开
            plates = item[8]  # 所属题材
            plate_names = "、".join(plate["name"] for plate in plates) if isinstance(plates, list) else ""
            
            # 几天几板
            m_days_n_boards = item[11] if len(item) > 11 else ""
            
            # 添加到处理后的数据列表
            processed_data.append({
                "code": code,
                "name": name,
                "description": description,
                "plates": plate_names,
                "m_days_n_boards": m_days_n_boards,
                "date": date_str
            })
            
        except Exception as e:
            logging.error(f"处理股票数据时出错: {e}, 数据项: {item}")
    
    # 存储到数据库
    if processed_data:
        db.store_stock_data(date_str, processed_data)
        logging.info(f"已将{date_str}的{len(processed_data)}条股票数据存储到数据库")

if __name__ == "__main__":
    crawl_stock_data()