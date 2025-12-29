#!/usr/bin/env python3
# 直接测试我们新增的测试接口
import requests
import json

# 测试新增的测试接口
def test_api():
    # 测试新增的测试接口
    test_url = 'http://localhost:5000/api/test-realtime-stock'
    
    print(f'测试新增接口: {test_url}')
    
    try:
        response = requests.get(test_url)
        print(f'API响应状态码: {response.status_code}')
        
        if response.status_code == 200:
            try:
                data = response.json()
                print('API响应数据:')
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # 检查数据结构是否正确
                if 'data' in data and data['data'] and 'items' in data['data'] and isinstance(data['data']['items'], list):
                    print(f'数据格式正确，包含 {len(data["data"]["items"])} 条股票数据')
                    
                    # 显示每条记录的关键信息
                    for i, item in enumerate(data['data']['items']):
                        symbol = item.get('symbol', '未知')
                        current = item.get('current', '未知')
                        percent = item.get('percent', '未知')
                        print(f'{i+1}. 代码: {symbol}, 价格: {current}, 涨幅: {percent}')
                else:
                    print('警告：响应数据结构不符合预期')
                    print('完整响应:', data)
            except json.JSONDecodeError:
                print('错误：无法解析JSON响应')
                print('原始响应内容:', response.text)
        else:
            print(f'API返回错误状态: {response.status_code}')
            print('错误响应:', response.text)
            
    except requests.exceptions.RequestException as e:
        print(f'请求API失败: {e}')

# 执行测试
if __name__ == '__main__':
    test_api()
