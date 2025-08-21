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
ollama pull qwen3:4b
ollama pull gemma3:270m
ollama pull llama3.1:8b
```

### 查看已安裝的模型
```bash
ollama ls
```

### 移除模型
```bash
ollama rm qwen2.5:3b
```

### 測試模型
```bash
ollama run gpt-oss:20b
```

## 模型規格參考

NAME             ID              SIZE      MODIFIED    
gemma3:270m      b16d6d39dfbd    241 MB    6 days ago     
qwen3:4b         e55aed6fe643    2.5 GB    13 days ago    
gemma3:latest    a2af6cc3eb7f    3.3 GB    13 days ago    
gpt-oss:20b      f2b8351c629c    13 GB     2 weeks ago    
qwen2.5:3b       357c53fb659c    1.9 GB    2 weeks ago    

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