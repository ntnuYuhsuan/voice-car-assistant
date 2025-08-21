# Ollama 使用指南

## 基本指令

### 安裝 Ollama
```bash
brew install ollama
```

### 啟動 Ollama 服務
```bash
ollama serve
```

### 下載模型
```bash
# 下載預設的 qwen2.5:3b 模型
ollama pull qwen2.5:3b

# 下載其他模型
ollama pull qwen2.5:7b
ollama pull qwen2.5:14b
ollama pull gemma2:2b
ollama pull gemma2:9b
ollama pull llama3.1:8b
```

### 查看已安裝的模型
```bash
ollama list
```

### 移除模型
```bash
ollama rm qwen2.5:3b
```

### 測試模型
```bash
ollama run qwen2.5:3b
```

## 常用模型規格

| 模型名稱 | 參數量 | 記憶體需求 | 適用場景 |
|----------|--------|------------|----------|
| qwen2.5:1.5b | 1.5B | ~2GB | 輕量級應用 |
| qwen2.5:3b | 3B | ~4GB | 平衡性能與資源 |
| qwen2.5:7b | 7B | ~8GB | 高品質回答 |
| qwen2.5:14b | 14B | ~16GB | 最佳性能 |
| gemma2:2b | 2B | ~3GB | Google 模型 |
| llama3.1:8b | 8B | ~10GB | Meta 模型 |

## 服務管理

### 檢查服務狀態
```bash
ps aux | grep ollama
```

### 停止服務
```bash
killall ollama
```

### 重啟服務
```bash
killall ollama
ollama serve &
```

## 進階使用

### 自定義模型配置
創建 Modelfile 進行客製化設定：
```bash
# 創建自定義模型配置
cat > Modelfile << EOF
FROM qwen2.5:3b
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "你是一個專業的車載語音助理。"
EOF

# 創建自定義模型
ollama create custom-car-assistant -f Modelfile
```

### API 使用
```bash
# 透過 API 測試模型
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:3b",
  "prompt": "你好，我是車載助理"
}'
```