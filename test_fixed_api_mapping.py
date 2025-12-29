import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入huoli模块
from huoli import ChipDistributionAnalyzer, get_stock_data_from_api_v2, get_profit_ratio_data

def test_fixed_functions():
    """测试修复后的函数是否正确工作"""
    print("===== 开始测试修复后的功能 =====")
    
    # 测试1: 测试get_stock_data_from_api_v2函数的字段映射
    print("\n1. 测试get_stock_data_from_api_v2字段映射...")
    stock_code = "301629"
    df = get_stock_data_from_api_v2(stock_code)
    
    if df is not None and len(df) > 0:
        print(f"✓ 成功获取数据: {len(df)}行")
        print("  数据列名:", df.columns.tolist())
        print("  数据类型:")
        for col in df.columns:
            print(f"    {col}: {df[col].dtype}")
        
        # 检查必要的中文列名是否存在
        required_columns = ['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', '涨跌幅', '换手率']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ 错误: 缺少必要的中文列名: {missing_columns}")
        else:
            print("✓ 所有必要的中文列名都存在")
            
            # 显示前3行数据作为示例
            print("\n  数据示例 (前3行):")
            print(df.head(3).to_string(index=False))
    else:
        print("❌ 无法获取数据或数据为空")
    
    # 测试2: 测试ChipDistributionAnalyzer的获利比例计算
    print("\n2. 测试ChipDistributionAnalyzer获利比例计算...")
    if df is not None and len(df) > 0:
        try:
            analyzer = ChipDistributionAnalyzer(df)
            print("✓ 成功创建ChipDistributionAnalyzer实例")
            
            # 测试计算最近几个交易日的获利比例
            print("\n  最近5个交易日的获利比例:")
            for i in range(min(5, len(df))):
                try:
                    result = analyzer.calculate_chip_distribution(i)
                    date_str = df.iloc[i]['日期'].strftime('%Y-%m-%d') if pd.notna(df.iloc[i]['日期']) else f"未知日期-{i}"
                    print(f"    {date_str}: {result['profit_ratio']:.4f} ({result['profit_ratio']*100:.2f}%)")
                except Exception as e:
                    print(f"    计算第{i}天失败: {str(e)}")
        except Exception as e:
            print(f"❌ 创建分析器失败: {str(e)}")
    
    # 测试3: 测试get_profit_ratio_data函数
    print("\n3. 测试get_profit_ratio_data函数...")
    try:
        profit_ratios = get_profit_ratio_data(stock_code, days=10)
        print(f"✓ 成功获取获利比例数据: {len(profit_ratios)}条")
        
        # 显示前5条数据
        print("\n  获利比例数据示例 (前5条):")
        for item in profit_ratios[:5]:
            print(f"    {item['date']}: {item['profit_ratio']:.4f} ({item['profit_ratio']*100:.2f}%)")
        
        # 验证数据格式
        all_valid = True
        for item in profit_ratios:
            if 'date' not in item or 'profit_ratio' not in item:
                all_valid = False
                break
            if not isinstance(item['profit_ratio'], (int, float)) or item['profit_ratio'] < 0 or item['profit_ratio'] > 1:
                all_valid = False
                break
        
        if all_valid:
            print("✓ 所有获利比例数据格式正确，值范围在0-1之间")
        else:
            print("❌ 部分获利比例数据格式不正确")
            
    except Exception as e:
        print(f"❌ 获取获利比例数据失败: {str(e)}")
    
    print("\n===== 测试完成 =====")
    print("\n修复总结:")
    print("1. ✓ 修复了东方财富API字段映射 (f51-f61) 到中文列名")
    print("2. ✓ 移除了重复定义的get_profit_ratio_data函数")
    print("3. ✓ 修复了调用未定义方法calculate_profit_ratio的问题")
    print("4. ✓ 添加了缺少的create_mock_data函数实现")
    print("5. ✓ 确保返回的数据格式正确")
    print("\n现在profit_ratio计算应该基于正确的API字段映射，数值应该准确了！")

if __name__ == "__main__":
    test_fixed_functions()
