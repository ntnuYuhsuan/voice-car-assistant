#!/usr/bin/env python3
"""
測試Ollama服務連接
"""

import httpx
from rich.console import Console

console = Console()

async def test_ollama_connection():
    """測試Ollama API連接"""
    try:
        async with httpx.AsyncClient() as client:
            # 測試服務狀態
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json()
                console.print("✅ Ollama服務運行正常")
                console.print("可用模型:")
                for model in models.get('models', []):
                    console.print(f"  - {model['name']}")
                return True
            else:
                console.print(f"❌ Ollama連接失敗: {response.status_code}")
                return False
                
    except Exception as e:
        console.print(f"❌ 無法連接到Ollama: {e}")
        console.print("請確保Ollama服務已啟動: ollama serve")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ollama_connection())