import pandas as pd
import numpy as np
from huoli import ChipDistributionAnalyzer

def test_profit_ratio_calculation():
    """测试获利比例计算逻辑"""
    print("开始测试获利比例计算逻辑...")
    
    # 创建测试数据
    test_data = []
    for i in range(10):
        test_data.append({
            '日期': pd.Timestamp.now() - pd.Timedelta(days=9-i),
            '开盘': 100 + i * 2,
            '收盘': 102 + i * 2,
            '最高': 104 + i * 2,
            '最低': 98 + i * 2,
            '成交量': 1000000,
            '换手率': 1.5
        })
    
    df = pd.DataFrame(test_data)
    print("测试数据创建完成")
    print(df)
    
    # 创建分析器
    analyzer = ChipDistributionAnalyzer(df, accuracy_factor=100, calc_range=10)
    
    # 测试_calculate_distribution_metrics方法
    print("\n测试_calculate_distribution_metrics方法:")
    distribution = [0.1] * 100  # 模拟均匀分布的筹码
    price_range = [95 + i * 0.5 for i in range(100)]
    current_price = 120.0
    
    metrics = analyzer._calculate_distribution_metrics(distribution, price_range, current_price)
    print(f"当前价格: {current_price}")
    print(f"获利比例: {metrics['profit_ratio']:.4f} ({metrics['profit_ratio']*100:.2f}%)")
    print(f"预期结果: 应该接近1.0，因为所有价格都低于当前价格")
    
    # 测试_calculate_key_metrics方法
    print("\n测试_calculate_key_metrics方法:")
    key_metrics = analyzer._calculate_key_metrics(distribution, price_range, current_price)
    print(f"当前价格: {current_price}")
    print(f"获利比例: {key_metrics['profit_ratio']:.4f} ({key_metrics['profit_ratio']*100:.2f}%)")
    print(f"预期结果: 应该接近1.0，因为所有价格都低于当前价格")
    
    # 测试边界情况 - 当前价格低于所有筹码价格
    print("\n测试边界情况 - 当前价格低于所有筹码价格:")
    current_price_low = 90.0
    metrics_low = analyzer._calculate_distribution_metrics(distribution, price_range, current_price_low)
    print(f"当前价格: {current_price_low}")
    print(f"获利比例: {metrics_low['profit_ratio']:.4f} ({metrics_low['profit_ratio']*100:.2f}%)")
    print(f"预期结果: 应该接近0.0，因为所有价格都高于当前价格")
    
    # 测试边界情况 - 当前价格在中间位置
    print("\n测试边界情况 - 当前价格在中间位置:")
    current_price_mid = 107.5  # 应该在中间位置
    metrics_mid = analyzer._calculate_distribution_metrics(distribution, price_range, current_price_mid)
    print(f"当前价格: {current_price_mid}")
    print(f"获利比例: {metrics_mid['profit_ratio']:.4f} ({metrics_mid['profit_ratio']*100:.2f}%)")
    print(f"预期结果: 应该接近0.5，因为大约一半的价格低于当前价格")
    
    # 测试真实K线数据
    print("\n测试真实K线数据:")
    for i in range(5, 10):
        try:
            result = analyzer.calculate_chip_distribution(i)
            print(f"\n日期: {df.iloc[i]['日期']}")
            print(f"收盘价: {df.iloc[i]['收盘']}")
            print(f"获利比例: {result['profit_ratio']:.4f} ({result['profit_ratio']*100:.2f}%)")
            print(f"平均成本: {result['avg_cost']:.2f}")
        except Exception as e:
            print(f"计算失败: {e}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_profit_ratio_calculation()
