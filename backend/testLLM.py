import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_api_connection():
    """测试API连接"""
    
    # 从环境变量获取配置
    api_key = os.getenv('LLM_API_KEY')
    base_url = os.getenv('LLM_BASE_URL')
    model_id = os.getenv('LLM_MODEL_ID', 'qwen-plus')
    
    print("正在测试API连接...")
    print(f"API Key: {api_key[:8]}..." if api_key else "API Key: 未设置")
    print(f"Base URL: {base_url}")
    print(f"Model ID: {model_id}")
    
    if not api_key or not base_url:
        print("错误: 缺少必要的环境变量 LLM_API_KEY 或 LLM_BASE_URL")
        return False
    
    # 测试API连接
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 发送一个简单的测试请求
    data = {
        'model': model_id,
        'messages': [
            {'role': 'user', 'content': '你好，请回复"连接成功"'}
        ],
        'temperature': 0.1,
        'max_tokens': 50
    }
    
    try:
        print("\n发送测试请求...")
        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"✓ API连接成功！")
                print(f"模型回复: {content}")
                return True
            else:
                print(f"✗ API响应格式异常: {result}")
                return False
        else:
            print(f"✗ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ 网络请求错误: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ 发生未知错误: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_connection()
    if success:
        print("\n✓ API连接测试成功！您的配置可以正常使用。")
    else:
        print("\n✗ API连接测试失败，请检查配置。")