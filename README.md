# 車載語音助理 (Voice Car Assistant)

基於 faster-whisper 和 Ollama 的中英文車載語音助理系統，採用本地部署架構。

## 特色功能

- **本地語音識別**: 採用 faster-whisper 模型進行中英文語音識別
- **本地 LLM 部署**: 基於 Ollama 運行本地大語言模型，支援彈性的模型參數設置
- **OpenAI API 整合**: 支援 OpenAI API 呼叫，可與本地模型並行使用
- **車載語音控制**: 支援車窗、空調、導航、娛樂等控制指令
- **隱私保護**: 完全本地運行，語音數據不外傳
- **VAD 檢測**: 智慧語音活動檢測，自動開始/停止錄音

## 系統需求

### 開發環境
- **作業系統**: macOS 15+
- **處理器**: M3 Apple Silicon
- **記憶體**: 16GB RAM
- **存儲空間**: 10GB 可用空間
- **麥克風**: 標準麥克風設備

## 安裝步驟

### 1. 克隆專案
```bash
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant
```

### 2. 設置 Anaconda 虛擬環境
```bash
conda create -n car-assistant python=3.11
conda activate car-assistant
pip install -r requirements_car_assistant.txt
```

### 3. 安裝 faster-whisper
faster-whisper 會根據指定的模型參數自動下載模型檔案：

| 模型大小 | 檔案大小 | 記憶體使用 |
|---------|---------|-----------|
| tiny    | 39 MB   | ~1 GB     |
| base    | 74 MB   | ~1 GB     |
| small   | 244 MB  | ~2 GB     |
| medium  | 769 MB  | ~5 GB     |
| large   | 1550 MB | ~10 GB    |

### 4. 安裝和設置 Ollama
```bash
brew install ollama
ollama serve &
ollama pull qwen2.5:3b
```

詳細的 Ollama 使用指南請參考 [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md)

## 使用方法

### 參數說明

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `--whisper-model` | `base` | Whisper 模型大小 (tiny/base/small/medium/large) |
| `--ollama-model` | `qwen2.5:3b` | Ollama 模型名稱 |
| `--use-openai` | `False` | 是否啟用 OpenAI API |
| `--openai-model` | `gpt-4o-mini` | OpenAI 模型名稱 |

### 執行指令範例

#### 基本執行
```bash
python car_assistant.py
```

#### 指定 Whisper 模型
```bash
python car_assistant.py --whisper-model medium
```

#### 指定 Ollama 模型
```bash
python car_assistant.py --ollama-model gemma2:latest
```

#### 啟用 OpenAI API
```bash
export OPENAI_API_KEY=your_api_key_here
python car_assistant.py --use-openai
```

#### 完整參數組合
```bash
python car_assistant.py --whisper-model medium --ollama-model gemma2:latest --use-openai --openai-model gpt-4o-mini
```

## 支援的車載指令

### 車窗控制
- "開前左車窗" / "關閉右邊車窗"
- "打開所有車窗" / "關閉車窗"

### 空調控制
- "設定溫度22度" / "調高溫度"
- "打開冷氣" / "關閉空調"
- "風速調到3" / "增強風速"

### 導航功能
- "導航到台北車站"
- "最快路線到桃園機場"
- "回家" / "去公司"

### 娛樂控制
- "播放音樂" / "暫停音樂"
- "下一首歌" / "上一首"
- "播放周杰倫的歌"

### 通訊功能
- "撥打電話給小明"
- "發送訊息給媽媽說我快到了"

### 車輛資訊
- "油量還剩多少"
- "引擎溫度正常嗎"
- "前方路況如何"