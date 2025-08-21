# 車載語音助理 (Voice Car Assistant)

基於 faster-whisper 和 Ollama 的中英文車載語音助理系統，採用本地部署架構。

## ✨ 特色功能

- 🎤 **中英文語音識別**: 採用 faster-whisper 模型，支援繁體中文和英文語音輸入
- 🤖 **本地 LLM 部署**: 基於 Ollama 運行本地大語言模型，支援彈性的模型參數設置
- 🔄 **OpenAI API 整合**: 支援 OpenAI API 呼叫，可與本地模型並行使用，雙引擎智慧回應
- 🚗 **車載語音控制**: 支援車窗、空調、導航、娛樂等智慧控制指令
- 🔒 **隱私保護**: 完全本地運行，語音數據不外傳，保障個人隱私
- 🎯 **VAD 檢測**: 智慧語音活動檢測，自動開始/停止錄音，無需手動操作

## 💻 系統需求

### 最低配置
- **作業系統**: Windows 10+ / macOS 15+
- **記憶體**: 8GB RAM (建議 16GB)
- **存儲空間**: 10GB 可用空間
- **麥克風**: 標準麥克風設備

### 建議配置
- **記憶體**: 16GB RAM
- **處理器**: M3 Apple Silicon / Intel i5+ / AMD Ryzen 5+
- **GPU**: NVIDIA RTX 系列 (支援 CUDA 加速)

## 🚀 安裝步驟

### 1. 克隆專案
```bash
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant
```

### 2. 設置虛擬環境

#### macOS 用戶
```bash
conda create -n car-assistant python=3.11
conda activate car-assistant
pip install -r requirements_car_assistant.txt
```

#### Windows 用戶
```cmd
conda create -n car-assistant python=3.11
conda activate car-assistant
pip install -r requirements_car_assistant.txt
```

### 3. 安裝 faster-whisper
faster-whisper 會根據指定的模型參數自動下載模型檔案：

| 模型大小 | 檔案大小 | GPU記憶體(VRAM) | CPU記憶體(RAM) | 相對速度 | 適用場景 |
|---------|---------|----------------|----------------|----------|----------|
| tiny    | 39 MB   | ~500 MB        | ~1 GB          | ~32x     | 快速測試、資源受限環境 |
| base    | 74 MB   | ~700 MB        | ~1 GB          | ~16x     | 輕量級應用、即時轉錄 |
| small   | 244 MB  | ~1.5 GB        | ~2 GB          | ~6x      | 一般用途、平衡性能 |
| medium  | 769 MB  | ~2.5 GB        | ~3 GB          | ~2x      | 中等準確度需求 |
| large   | 1550 MB | ~4.7 GB        | ~4 GB          | 1x       | 高準確度、生產環境 |

*基準測試環境：RTX 3070 Ti 8GB，13分鐘音檔*

### 4. 安裝和設置 Ollama

#### macOS 用戶
```bash
brew install ollama
ollama serve &
ollama pull qwen2.5:3b
```

#### Windows 用戶
1. 下載 [Ollama Windows 安裝程式](https://ollama.com/download/windows)
2. 執行 `OllamaSetup.exe` 並完成安裝
3. 開啟命令提示字元或 PowerShell：
```cmd
ollama serve
```
4. 開啟新的終端視窗下載模型：
```cmd
ollama pull qwen2.5:3b
```

詳細的 Ollama 使用指南請參考 [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md)

## 🎯 使用方法

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
# macOS / Linux
python car_assistant.py

# Windows
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

**macOS / Linux:**
```bash
export OPENAI_API_KEY=your_api_key_here
python car_assistant.py --use-openai
```

**Windows:**
```cmd
set OPENAI_API_KEY=your_api_key_here
python car_assistant.py --use-openai
```

#### 完整參數組合
```bash
python car_assistant.py --whisper-model medium --ollama-model gemma2:latest --use-openai --openai-model gpt-4o-mini
```

### 💡 快速啟動指南

1. **啟動 Ollama 服務** (確保在背景運行)
2. **啟動車載助理**: `python car_assistant.py`
3. **開始對話**: 系統自動檢測語音輸入
4. **退出程式**: 按 `Ctrl+C`

## 🚗 支援的車載指令

### 🪟 車窗控制
- "開前左車窗" / "關閉右邊車窗"
- "打開所有車窗" / "關閉車窗"

### ❄️ 空調控制
- "設定溫度22度" / "調高溫度"
- "打開冷氣" / "關閉空調"
- "風速調到3" / "增強風速"

### 🗺️ 導航功能
- "導航到台北車站"
- "最快路線到桃園機場"
- "回家" / "去公司"

### 🎵 娛樂控制
- "播放音樂" / "暫停音樂"
- "下一首歌" / "上一首"
- "播放周杰倫的歌"

### 📞 通訊功能
- "撥打電話給小明"
- "發送訊息給媽媽說我快到了"

### 🚘 車輛資訊
- "油量還剩多少"
- "引擎溫度正常嗎"
- "前方路況如何"

## 🛠️ Windows 特別注意事項

### 麥克風權限設置
1. 開啟 **設定** → **隱私權** → **麥克風**
2. 確保 **允許應用程式存取您的麥克風** 已開啟
3. 允許 **命令提示字元** 或 **PowerShell** 使用麥克風

### CUDA 加速 (選用)
如果您有 NVIDIA GPU，可以安裝 CUDA 版本的依賴：
```cmd
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 常見問題排解

#### Ollama 服務無法啟動
```cmd
# 檢查 Ollama 版本
ollama --version

# 手動啟動服務
ollama serve

# 檢查服務狀態
tasklist | findstr ollama
```

#### 虛擬環境問題
```cmd
# 重新建立環境
conda deactivate
conda remove -n car-assistant --all
conda create -n car-assistant python=3.11
conda activate car-assistant
pip install -r requirements_car_assistant.txt
```