// 测试实时股票数据API接口
const https = require('https');
const http = require('http');

// 测试API接口 - 使用少量股票代码
const testApi = () => {
    // 使用一些常见的股票代码进行测试
    const testSymbols = '600036.SS,600519.SS,000858.SZ,000001.SZ';
    const apiUrl = `http://localhost:5000/api/realtime-stock-data?symbols=${testSymbols}`;
    
    console.log(`测试API: ${apiUrl}`);
    
    http.get(apiUrl, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        res.on('end', () => {
            try {
                console.log('API响应状态码:', res.statusCode);
                
                if (res.statusCode === 200) {
                    const responseData = JSON.parse(data);
                    console.log('API响应数据:', JSON.stringify(responseData, null, 2));
                    
                    // 检查数据结构是否正确
                    if (responseData && responseData.data && Array.isArray(responseData.data.items)) {
                        console.log('数据格式正确，包含', responseData.data.items.length, '条股票数据');
                    } else {
                        console.log('警告：响应数据结构不符合预期');
                        console.log('完整响应:', responseData);
                    }
                } else {
                    console.log('API返回错误状态:', res.statusCode);
                    console.log('错误响应:', data);
                }
            } catch (error) {
                console.error('解析API响应失败:', error);
                console.log('原始响应:', data);
            }
        });
    }).on('error', (error) => {
        console.error('请求API失败:', error.message);
    });
};

// 执行测试
testApi();
