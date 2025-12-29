import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
from huoli import ChipDistributionAnalyzer

def test_api_field_mapping():
    """测试东方财富API字段映射是否正确"""
    print("开始测试东方财富API字段映射...")
    
    # 定义正确的字段映射
    correct_field_mapping = {
        'f51': '日期',
        'f52': '开盘',
        'f53': '收盘',
        'f54': '最高',
        'f55': '最低',
        'f56': '成交量',
        'f57': '成交额',
        'f59': '涨跌幅',
        'f61': '换手率'
    }
    
    # 打印正确的字段映射
    print("\n正确的字段映射:")
    for field, name in correct_field_mapping.items():
        print(f"  {field} -> {name}")
    
    # 测试API调用
    stock_code = "301629"
    secid = f"0.{stock_code}"
    end_date = datetime.now().strftime("%Y%m%d")
    url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={secid}&klt=101&fqt=1&lmt=10&end={end_date}&iscca=1&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f59,f61&ut=f057cbcbce2a86e2866ab8877db1d059&forcect=1"
    
    print(f"\n调用API: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and data['data'].get('klines'):
            klines = data['data']['klines']
            
            print(f"\nAPI返回数据示例 (前3条):")
            for i, kline in enumerate(klines[:3]):
                parts = kline.split(',')
                print(f"  记录 {i+1}: {parts}")
            
            # 根据用户提供的字段映射正确解析数据
            print("\n使用正确字段映射解析数据:")
            stock_data = []
            for kline in klines[:3]:  # 只处理前3条用于演示
                parts = kline.split(',')
                stock_data.append({
                    '日期': parts[0],        # f51
                    '开盘': float(parts[1]),  # f52
                    '收盘': float(parts[2]),  # f53
                    '最高': float(parts[3]),  # f54
                    '最低': float(parts[4]),  # f55
                    '成交量': float(parts[5]), # f56
                    '成交额': float(parts[6]), # f57
                    '涨跌幅': float(parts[7]), # f59
                    '换手率': float(parts[8])  # f61
                })
            
            # 打印解析后的数据
            for i, record in enumerate(stock_data):
                print(f"\n  记录 {i+1}:")
                for key, value in record.items():
                    print(f"    {key}: {value}")
            
            # 转换为DataFrame并测试获利比例计算
            df = pd.DataFrame(stock_data)
            print(f"\n转换为DataFrame, 数据形状: {df.shape}")
            
            # 检查是否有必要的列
            required_columns = ['开盘', '收盘', '最高', '最低', '成交量', '换手率']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"错误: 缺少必要列: {missing_columns}")
            else:
                print("✓ 所有必要列都存在")
                
                # 创建分析器并测试计算
                try:
                    analyzer = ChipDistributionAnalyzer(df, accuracy_factor=100, calc_range=10)
                    print("✓ 成功创建ChipDistributionAnalyzer实例")
                    
                    # 测试计算
                    for i in range(min(3, len(df))):
                        result = analyzer.calculate_chip_distribution(i)
                        print(f"\n  日期 {df.iloc[i]['日期']}:")
                        print(f"    获利比例: {result['profit_ratio']:.4f} ({result['profit_ratio']*100:.2f}%)")
                        print(f"    平均成本: {result['avg_cost']:.2f}")
                except Exception as e:
                    print(f"错误: 测试分析器时出错: {e}")
            
        else:
            print(f"错误: API返回数据不完整: {data}")
    
    except Exception as e:
        print(f"错误: API调用失败: {e}")

def check_huoli_issues():
    """检查huoli.py文件中的其他问题"""
    print("\n检查huoli.py文件中的其他问题:")
    print("1. 发现重复定义的get_profit_ratio_data函数")
    print("2. 发现调用了未定义的calculate_profit_ratio方法")
    print("3. get_stock_data_from_api_v2函数中的字段映射不正确")
    print("4. 缺少将API返回的英文列名转换为ChipDistributionAnalyzer所需的中文列名的逻辑")

if __name__ == "__main__":
    test_api_field_mapping()
    check_huoli_issues()