#!/usr/bin/env python3
"""
OpenAI API 測試腳本
測試 GPT-4o-mini API 連接、回應和超時問題
"""

import os
import asyncio
import time
from openai import OpenAI
import httpx

def test_sync_openai():
    """測試同步 OpenAI API 調用"""
    print("🧪 測試同步 OpenAI API...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ 未找到 OPENAI_API_KEY 環境變數")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        start_time = time.time()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一個測試助手，請簡短回應。"},
                {"role": "user", "content": "測試連接"}
            ],
            temperature=0.7,
            max_tokens=50,
            timeout=30  # 設置30秒超時
        )
        end_time = time.time()
        
        print(f"✅ 同步調用成功 (耗時: {end_time - start_time:.2f}秒)")
        print(f"📝 回應: {response.choices[0].message.content.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ 同步調用失敗: {e}")
        return False

async def test_async_openai():
    """測試異步 OpenAI API 調用（使用 executor）"""
    print("\n🧪 測試異步 OpenAI API (executor)...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ 未找到 OPENAI_API_KEY 環境變數")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        start_time = time.time()
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一個測試助手，請簡短回應。"},
                    {"role": "user", "content": "測試異步連接"}
                ],
                temperature=0.7,
                max_tokens=50,
                timeout=30
            )
        )
        end_time = time.time()
        
        print(f"✅ 異步調用成功 (耗時: {end_time - start_time:.2f}秒)")
        print(f"📝 回應: {response.choices[0].message.content.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ 異步調用失敗: {e}")
        return False

async def test_async_with_timeout():
    """測試帶超時控制的異步調用"""
    print("\n🧪 測試異步超時控制...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ 未找到 OPENAI_API_KEY 環境變數")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        start_time = time.time()
        # 使用 asyncio.wait_for 控制整體超時
        response = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一個測試助手，請簡短回應。"},
                        {"role": "user", "content": "測試超時控制"}
                    ],
                    temperature=0.7,
                    max_tokens=50,
                    timeout=15  # OpenAI client 超時
                )
            ),
            timeout=20  # asyncio 總超時
        )
        end_time = time.time()
        
        print(f"✅ 超時控制調用成功 (耗時: {end_time - start_time:.2f}秒)")
        print(f"📝 回應: {response.choices[0].message.content.strip()}")
        return True
        
    except asyncio.TimeoutError:
        print("❌ 調用超時")
        return False
    except Exception as e:
        print(f"❌ 調用失敗: {e}")
        return False

def test_network_connectivity():
    """測試網路連線"""
    print("\n🧪 測試網路連線...")
    
    try:
        import requests
        response = requests.get("https://api.openai.com/v1/models", timeout=10)
        if response.status_code == 401:  # Unauthorized是預期的（沒有API key）
            print("✅ 網路連線正常（OpenAI API 可達）")
            return True
        else:
            print(f"⚠️ 意外狀態碼: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 網路連線失敗: {e}")
        return False

async def main():
    """主測試函數"""
    print("🚀 OpenAI API 連接測試開始\n")
    
    # 檢查環境變數
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ 請設置 OPENAI_API_KEY 環境變數")
        print("   export OPENAI_API_KEY='your-api-key'")
        return
    
    # 測試序列
    tests = [
        ("網路連線", test_network_connectivity),
        ("同步調用", test_sync_openai),
        ("異步調用", test_async_openai),
        ("超時控制", test_async_with_timeout)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 {test_name} 測試")
        print('='*50)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
            results[test_name] = False
    
    # 結果總結
    print(f"\n{'='*50}")
    print("📊 測試結果總結")
    print('='*50)
    
    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
    
    success_count = sum(1 for r in results.values() if r)
    total_count = len(results)
    
    print(f"\n🎯 總體結果: {success_count}/{total_count} 測試通過")
    
    if success_count == total_count:
        print("🎉 所有測試通過！OpenAI API 連接正常。")
    else:
        print("⚠️ 部分測試失敗，請檢查網路連接和API金鑰。")

if __name__ == "__main__":
    asyncio.run(main())