import db
import sqlite3
import datetime

# 测试数据
TEST_DATE = datetime.datetime.now().strftime("%Y%m%d")

# 创建初始测试股票数据（题材较少）
initial_stocks = [
    {
        "code": "000001",
        "name": "平安银行",
        "description": "银行",
        "plates": "银行",  # 1个题材
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
    }
]

# 创建更新测试股票数据（题材较多）
update_stocks = [
    {
        "code": "000001",
        "name": "平安银行",
        "description": "银行",
        "plates": "银行,深圳成指,金融",  # 3个题材，应该更新
        "m_days_n_boards": "1",
        "date": TEST_DATE
    },
    {
        "code": "000002",
        "name": "万科A",
        "description": "地产",
        "plates": "地产",  # 1个题材，与原有相同，不更新
        "m_days_n_boards": "1",
        "date": TEST_DATE
    },
    {
        "code": "000003",
        "name": "ST宝安",
        "description": "地产",
        "plates": "地产,ST",  # 新股票
        "m_days_n_boards": "1",
        "date": TEST_DATE
    }
]

def test_update_deduplication():
    print(f"开始测试更新去重逻辑，测试日期：{TEST_DATE}")
    
    # 1. 先存储初始数据
    print("\n1. 存储初始数据（题材较少）")
    db.store_stock_data(TEST_DATE, initial_stocks)
    
    # 查看初始存储结果
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    
    table_name = f"stock_{TEST_DATE}"
    cursor.execute(f"SELECT code, name, plates FROM {table_name}")
    rows = cursor.fetchall()
    
    print("初始存储结果：")
    for row in rows:
        print(f"代码：{row[0]}, 名称：{row[1]}, 题材：{row[2]}, 题材数量：{len(row[2].split(','))}")
    
    conn.close()
    
    # 2. 再存储更新数据
    print("\n2. 存储更新数据（部分题材较多）")
    db.store_stock_data(TEST_DATE, update_stocks)
    
    # 查看更新后结果
    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT code, name, plates FROM {table_name}")
    rows = cursor.fetchall()
    
    print("更新后存储结果：")
    for row in rows:
        print(f"代码：{row[0]}, 名称：{row[1]}, 题材：{row[2]}, 题材数量：{len(row[2].split(','))}")
    
    # 验证平安银行是否更新为3个题材
    cursor.execute(f"SELECT plates FROM {table_name} WHERE name = '平安银行'")
    result = cursor.fetchone()
    if result:
        plates = result[0]
        plate_count = len(plates.split(','))
        print(f"\n平安银行题材数量：{plate_count}")
        if plate_count == 3:
            print("✅ 测试通过：成功更新为题材较多的记录")
        else:
            print("❌ 测试失败：没有更新为题材较多的记录")
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
    test_update_deduplication()