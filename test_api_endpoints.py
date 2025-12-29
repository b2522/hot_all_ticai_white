#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试后端API功能的脚本
"""

import requests
import json
import time

def test_profit_ratio_api():
    """测试获利比例API"""
    print("开始测试 /api/profit-ratio-data API...")
    
    # 定义测试参数
    stock_codes = ['301629', '600000', '000001']
    base_url = 'http://127.0.0.1:5000/api/profit-ratio-data'
    
    for stock_code in stock_codes:
        url = f"{base_url}?stock_code={stock_code}"
        print(f"\n测试股票代码: {stock_code}")
        print(f"请求URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"响应数据类型: {type(data)}")
                print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                
                # 验证数据格式
                if isinstance(data, dict):
                    if 'status' in data:
                        print(f"状态: {data['status']}")
                    if 'data' in data:
                        print(f"数据长度: {len(data['data']) if isinstance(data['data'], list) else 'N/A'}")
                    if 'message' in data:
                        print(f"消息: {data['message']}")
            else:
                print(f"请求失败: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
        
        time.sleep(2)  # 暂停2秒避免请求过快

def test_other_apis():
    """测试其他API端点"""
    print("\n开始测试其他API端点...")
    
    apis_to_test = [
        {'name': '首页', 'url': 'http://127.0.0.1:5000/'},
        {'name': '股票搜索', 'url': 'http://127.0.0.1:5000/search?q=科技'},
        # 可以添加更多API端点
    ]
    
    for api in apis_to_test:
        print(f"\n测试: {api['name']}")
        print(f"URL: {api['url']}")
        
        try:
            response = requests.get(api['url'], timeout=5)
            print(f"状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
        
        time.sleep(1)

if __name__ == '__main__':
    print("=======================")
    print("后端API测试脚本")
    print("=======================")
    
    try:
        # 先启动Flask服务器
        import subprocess
        import threading
        import sys
        
        print("启动Flask服务器...")
        server_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        print("等待服务器启动...")
        time.sleep(3)
        
        # 测试API
        try:
            test_profit_ratio_api()
            test_other_apis()
        except Exception as e:
            print(f"测试过程中出错: {e}")
        finally:
            # 关闭服务器
            print("\n关闭服务器...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                
    except Exception as e:
        print(f"脚本执行出错: {e}")
    
    print("\n测试完成！")
