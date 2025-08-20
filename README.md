# 車載語音助理 (Voice Car Assistant) 🚗🎤

基於 faster-whisper 和 Ollama 的中英文車載語音助理，專為駕駛者設計的智慧語音控制系統。

## ✨ 特色功能

- 🎤 **中英文語音識別**: 使用 faster-whisper 模型，支援繁體中文和英文
- 🤖 **本地 LLM**: 基於 Ollama 的離線大語言模型（qwen2.5:3b）
- 🔄 **雙模型支援**: 可選擇同時使用本地模型和 OpenAI GPT-4o-mini
- 📝 **純文字回覆**: 移除 TTS 語音合成，避免駕駛分心
- 🚗 **車載指令**: 支援開關車窗、調節溫度、導航、音樂控制等
- 🔒 **隱私保護**: 完全本地運行，語音數據不外傳
- 🎯 **VAD 檢測**: 智慧語音活動檢測，自動開始/停止錄音

## 🖥️ 系統需求

### 最低需求
- **作業系統**: Windows 10+ / macOS 10.15+ / Linux
- **Python**: 3.11+
- **記憶體**: 8GB RAM (建議 16GB)
- **存儲空間**: 10GB 可用空間
- **麥克風**: 任何標準麥克風或耳機麥克風

### 建議配置
- CPU: Intel i5 / AMD Ryzen 5 或以上
- RAM: 16GB
- SSD: 推薦使用 SSD 提升模型載入速度

## 🚀 快速開始

### 從 GitHub 克隆

```bash
# 克隆專案
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant

# 創建虛擬環境並安裝依賴
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安裝依賴
pip install -r requirements_car_assistant.txt
```

## 📦 詳細安裝步驟

### Windows 安裝

#### 1. 安裝 Python 3.11
```powershell
# 方法一：從官網下載 https://www.python.org/downloads/
# 方法二：使用 winget
winget install Python.Python.3.11
```

#### 2. 安裝 Git（如果尚未安裝）
```powershell
# 使用 winget
winget install Git.Git
```

#### 3. 克隆專案並設置環境
```powershell
# 克隆專案
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant

# 創建虛擬環境
python -m venv venv

# 啟用虛擬環境
venv\Scripts\activate

# 升級 pip
python -m pip install --upgrade pip

# 安裝依賴
pip install -r requirements_car_assistant.txt
```

#### 4. 安裝和設置 Ollama
```powershell
# 下載並安裝 Ollama for Windows
# 從官網下載：https://ollama.ai/download/windows
# 或使用 winget
winget install Ollama.Ollama

# 安裝完成後，打開新的命令提示字元或重啟當前終端
ollama serve

# 在另一個終端中下載模型
ollama pull qwen2.5:3b
```

#### 5. 測試安裝
```powershell
# 測試 Ollama 連接
python test_ollama.py

# 如果測試成功，啟動車載助理
python car_assistant.py
```

### macOS 安裝

#### 1. 安裝 Homebrew（如果尚未安裝）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安裝 Python 和依賴
```bash
# 安裝 Python 3.11
brew install python@3.11

# 克隆專案
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant

# 創建虛擬環境
python3.11 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements_car_assistant.txt
```

#### 3. 安裝 Ollama
```bash
# 安裝 Ollama
brew install ollama

# 啟動服務
ollama serve &

# 下載模型
ollama pull qwen2.5:3b
```

#### 4. 運行助理
```bash
python car_assistant.py
```

### Linux 安裝

#### 1. 安裝 Python 3.11
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# CentOS/RHEL/Fedora
sudo dnf install python3.11 python3.11-venv python3.11-devel
```

#### 2. 設置專案
```bash
# 克隆專案
git clone https://github.com/ntnuYuhsuan/voice-car-assistant.git
cd voice-car-assistant

# 創建虛擬環境
python3.11 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements_car_assistant.txt
```

#### 3. 安裝 Ollama
```bash
# 下載並安裝 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 啟動服務
ollama serve &

# 下載模型
ollama pull qwen2.5:3b
```

## 🎯 使用方法

### 基本使用
```bash
# 啟動車載助理（僅使用本地模型）
python car_assistant.py

# 使用不同的 Whisper 模型
python car_assistant.py --whisper-model medium

# 使用不同的 Ollama 模型
python car_assistant.py --ollama-model qwen2.5:7b
```

### 進階使用（雙模型）
```bash
# Windows 設置 OpenAI API Key
set OPENAI_API_KEY=your_api_key_here

# macOS/Linux 設置 OpenAI API Key
export OPENAI_API_KEY=your_api_key_here

# 啟動雙模型助理
python car_assistant.py --use-openai
```

### 操作流程
1. **啟動**: 運行 `python car_assistant.py`
2. **語音輸入**: 系統自動檢測語音，無需按鍵
3. **處理**: 系統自動進行語音識別和回應生成
4. **查看回應**: 文字回應顯示在終端
5. **退出**: 按 `Ctrl+C` 退出

## 🚗 支援的車載指令

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

## 🛠️ 故障排除

### Windows 常見問題

#### Ollama 無法啟動
```powershell
# 檢查 Ollama 是否正確安裝
ollama --version

# 手動啟動 Ollama 服務
ollama serve

# 檢查防火牆設置，確保 localhost:11434 可用
```

#### 麥克風權限問題
1. 開啟 **設定** > **隱私權** > **麥克風**
2. 確保 **允許應用程式存取您的麥克風** 已開啟
3. 允許 **命令提示字元** 或 **PowerShell** 使用麥克風

#### Python 環境問題
```powershell
# 檢查 Python 版本
python --version

# 如果顯示錯誤，嘗試使用完整路徑
C:\Python311\python.exe --version

# 重新安裝虛擬環境
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements_car_assistant.txt
```

### macOS/Linux 常見問題

#### 權限問題
```bash
# 給予麥克風權限（macOS）
# 系統偏好設定 > 安全性與隱私 > 隱私 > 麥克風

# 安裝音訊相關依賴（Linux）
sudo apt install portaudio19-dev python3-pyaudio
```

#### Ollama 服務問題
```bash
# 檢查 Ollama 狀態
ps aux | grep ollama

# 重啟 Ollama 服務
killall ollama
ollama serve &

# 檢查模型是否已下載
ollama list
```

### 一般故障排除

#### 語音識別準確度低
1. 確保環境較為安靜
2. 說話清晰，語速適中
3. 使用更大的 Whisper 模型：`--whisper-model large`
4. 檢查麥克風距離和品質

#### 回應速度慢
1. 使用較小的模型：`--ollama-model qwen2.5:3b`
2. 確保有足夠的系統記憶體
3. 關閉不必要的後台程序
4. 考慮使用 SSD 硬碟

#### 記憶體不足
```bash
# 監控記憶體使用
# Windows
tasklist /fi "imagename eq ollama.exe"

# macOS/Linux
top -p $(pgrep ollama)

# 如果記憶體不足，使用更小的模型
ollama pull qwen2.5:1.5b
python car_assistant.py --ollama-model qwen2.5:1.5b
```

## 🔧 技術架構

```
語音輸入 → VAD檢測 → Faster-Whisper → 文字處理 → Ollama/OpenAI → 格式化回應
```

### 核心組件
- **faster-whisper**: OpenAI Whisper 的優化版本，支援中英文語音識別
- **Ollama**: 本地 LLM 服務框架，運行 qwen2.5 模型
- **silero-vad**: 語音活動檢測，自動識別語音開始和結束
- **LangChain**: LLM 應用開發框架，管理對話歷史
- **Rich**: 終端介面美化和狀態顯示

## 📁 專案結構

```
voice-car-assistant/
├── car_assistant.py              # 主程式
├── requirements_car_assistant.txt # 依賴清單
├── test_ollama.py               # Ollama 連接測試
├── test_openai_api.py           # OpenAI API 測試
├── README.md                    # 本文檔
├── LICENSE                      # 許可證
└── .gitignore                   # Git 忽略清單
```

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 這個專案
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 📄 許可證

本專案採用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 文件

## 🙏 致謝

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - 高效的語音識別
- [Ollama](https://ollama.ai/) - 本地 LLM 服務
- [silero-vad](https://github.com/snakers4/silero-vad) - 語音活動檢測
- [LangChain](https://python.langchain.com/) - LLM 應用框架

## 📞 支援

如有問題或建議，請：
1. 查看 [FAQ](#故障排除) 部分
2. 搜尋現有的 [Issues](https://github.com/ntnuYuhsuan/voice-car-assistant/issues)
3. 創建新的 Issue 描述您的問題

---

**安全提醒**: 請在確保行車安全的前提下使用本系統，建議在停車狀態下進行初始設置和測試。🚗💨