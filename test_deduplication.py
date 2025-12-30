import db
import sqlite3
import datetime

# 测试数据
TEST_DATE = datetime.datetime.now().strftime("%Y%m%d")

# 创建一些测试股票数据
test_stocks = [
    {
        "code": "000001",
        "name": "平安银行",
        "description": "银行",
        "plates": "银行,深圳成指",  # 2个题材
        "m_days_n_boards": "1",
        "date": TEST_DATE
    },
    {
        "code": "000001",
        "name": "平安银行",
        "description": "银行",
        "plates": "银行,深圳成指,金融,大盘",  # 4个题材，应该保留这个
        "m_days_n_boards": "1",
        "date": TEST_DATE
    },
    {
        "code": "000002",
        "name": "万科A",
        "description": "地产",
        "plates": "地产",  # 1个题材
        "m_days_n_boards": "1",
        "date": TEST_DATE
    },
    {
        "code": "000003",
        "name": "ST宝安",
        "description": "地产",
        "plates": "地产,ST",  # 2个题材
        "m_days_n_boards": "1",
        "date": TEST_DATE
    }
]

def test_deduplication():
    print(f"开始测试去重逻辑，测试日期：{TEST_DATE}")
    
    # 存储测试数据
    db.store_stock_data(TEST_DATE, test_stocks)
    
    # 查看存储结果
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    
    table_name = f"stock_{TEST_DATE}"
    cursor.execute(f"SELECT code, name, plates FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f"\n存储结果（共{len(rows)}条记录）：")
    for row in rows:
        print(f"代码：{row[0]}, 名称：{row[1]}, 题材：{row[2]}, 题材数量：{len(row[2].split(','))}")
    
    # 验证平安银行是否保留了4个题材的记录
    cursor.execute(f"SELECT plates FROM {table_name} WHERE name = '平安银行'")
    result = cursor.fetchone()
    if result:
        plates = result[0]
        plate_count = len(plates.split(','))
        print(f"\n平安银行题材数量：{plate_count}")
        if plate_count == 4:
            print("✅ 测试通过：成功保留了题材较多的记录")
        else:
            print("❌ 测试失败：没有保留题材较多的记录")
    else:
        print("❌ 测试失败：没有找到平安银行的数据")
    
    conn.close()
    
    # 清理测试数据
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()
    print(f"\n测试完成，已清理测试表 {table_name}")

if __name__ == "__main__":
    test_deduplication()