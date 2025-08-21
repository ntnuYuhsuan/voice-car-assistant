#!/usr/bin/env python3
"""
車載語音助理 (Voice Car Assistant) - 基於 local-talking-llm (簡化版)
支援中英文語音識別，使用 faster-whisper，純文字回覆（無 TTS）
"""

import time
import threading
import numpy as np
from faster_whisper import WhisperModel
import sounddevice as sd
import argparse
from rich.console import Console
import asyncio
import httpx
from silero_vad import load_silero_vad, get_speech_timestamps
import openai
import os

# 現代化的LangChain導入
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_ollama import OllamaLLM

system_prompt = """你是車載智慧助理。專為台灣駕駛者設計，可處理中文車載指令。

安全原則：
- 絕對禁止自動駕駛指令
- 不執行危險或非法操作
- 台灣地區以外的導航請求將被拒絕

回復格式：簡潔、直接，符合駕駛情境

輸出規則：
1. 主要回應：<message>簡短回覆用戶(15字內)</message>
2. 指令執行：<command>FUNCTION_NAME(參數)</command>
3. 錯誤處理：<error>錯誤描述</error>

支援指令：
- OpenWindow(zone="位置", value="狀態") # 位置: FRONT_LEFT, FRONT_RIGHT, REAR_LEFT, REAR_RIGHT; 狀態: open, close
- SetFanSpeed(zone="區域", value=數值) # 區域: DRIVER, PASSENGER, REAR, ALL; 數值: 1-5
- SetNavigation(destination="目的地", type="類型") # 類型: address, poi, home, work
- SetTemperature(zone="區域", value=溫度) # 區域: DRIVER, PASSENGER, REAR, ALL; 溫度: 16-32
- PlayMusic(action="動作", target="目標") # 動作: play, pause, next, previous; 目標: 歌名/藝人
- MakeCall(contact="聯絡人") # 撥打電話
- SendMessage(contact="聯絡人", message="內容") # 發送訊息

範例格式：
用戶："開前左車窗"
<message>正在開啟車窗</message>
<command>OpenWindow(zone="FRONT_LEFT", value="open")</command>

用戶："設定溫度22度"
<message>調整溫度中</message>
<command>SetTemperature(zone="ALL", value=22.0)</command>

請嚴格按照此格式回應。"""

console = Console()

class CarVoiceAssistant:
    def __init__(self, whisper_model="medium", ollama_model="qwen2.5:3b", use_openai=False):
        self.whisper_model = whisper_model
        self.ollama_model = ollama_model
        self.use_openai = use_openai
        self.stt = None  # faster-whisper 模型
        self.llm = None
        self.chain_with_history = None
        self.chat_sessions = {}
        
        # OpenAI客戶端設置 - 一律從環境變數獲取API密鑰
        if self.use_openai:
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
            if self.openai_api_key:
                openai.api_key = self.openai_api_key
                self.openai_client = openai.OpenAI(api_key=self.openai_api_key)
                console.print("[green]✅ 環境變數載入")
            else:
                console.print("[red]❌ 環境變數 OPENAI_API_KEY 未設置，將僅使用本地模型")
                self.use_openai = False
        
        # VAD相關
        self.vad_model = None
        self.is_listening = False
        self.audio_buffer = []
        self.sample_rate = 16000
        self.silence_duration = 1.0
        
        # 車載系統狀態
        self.vehicle_state = {
            "speed": 0,
            "fuel_level": 75,
            "engine_temp": 90,
            "current_location": "台北市信義區",
            "destination": None,
            "traffic_condition": "正常",
            "weather": "晴朗"
        }
        
    async def initialize(self):
        """初始化所有組件 - 使用 faster-whisper"""
        console.print("[cyan]🚗 車載智慧助理初始化中...")
        
        # 載入VAD模型
        console.print("[yellow]載入VAD語音活動檢測模型...")
        try:
            vad_result = load_silero_vad(onnx=True)
            if isinstance(vad_result, tuple):
                self.vad_model, _ = vad_result
            else:
                self.vad_model = vad_result
            console.print("[green]✅ VAD模型載入成功")
        except Exception as e:
            console.print(f"[red]❌ VAD模型載入失敗: {e}")
            console.print("[yellow]將使用fallback模式（無VAD）")
        
        # 載入 Faster-Whisper 模型
        console.print(f"[yellow]載入 Faster-Whisper 模型: {self.whisper_model}")
        try:
            self.stt = WhisperModel(
                self.whisper_model,
                device="cpu",
                compute_type="int8",
                cpu_threads=0,
                num_workers=1
            )
            console.print("[green]✅ Faster-Whisper 載入成功")
        except Exception as e:
            console.print(f"[red]❌ Faster-Whisper 載入失敗: {e}")
            raise
        
        # 測試Ollama連接
        await self.test_ollama_connection()
        
        # 初始化LLM
        self.setup_llm()
        
        console.print("[green]✅ 智慧助理初始化完成")
        console.print("[cyan]🎤 系統背景監聽中...")
        
    async def test_ollama_connection(self):
        """測試Ollama服務連接"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json()
                    console.print("[green]✅ Ollama服務連接成功")
                    available_models = [m['name'] for m in models.get('models', [])]
                    if self.ollama_model not in available_models:
                        console.print(f"[yellow]⚠️ 模型 {self.ollama_model} 未找到")
                        if available_models:
                            console.print(f"[blue]可用模型: {', '.join(available_models[:3])}")
                            # 使用第一個可用模型
                            self.ollama_model = available_models[0]
                            console.print(f"[blue]將使用: {self.ollama_model}")
                else:
                    raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            console.print(f"[red]❌ Ollama連接失敗: {e}")
            console.print("[yellow]請確保Ollama服務已啟動: ollama serve")
            raise
    
    def setup_llm(self):
        """設置LLM對話鏈"""
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 初始化LLM
        self.llm = OllamaLLM(model=self.ollama_model, base_url="http://localhost:11434")
        
        # 創建對話鏈
        chain = prompt_template | self.llm
        
        # 添加歷史記錄功能
        self.chain_with_history = RunnableWithMessageHistory(
            chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
    
    def get_session_history(self, session_id: str) -> InMemoryChatMessageHistory:
        """獲取或創建對話歷史"""
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = InMemoryChatMessageHistory()
        return self.chat_sessions[session_id]
    
    def transcribe_chinese(self, audio_np: np.ndarray) -> str:
        """使用 faster-whisper 轉錄音訊為中英文文字"""
        try:
            # 使用 faster-whisper 進行轉錄，支援中英文
            segments, info = self.stt.transcribe(
                audio_np,
                language=None,  # 自動檢測語言（中英文）
                task="transcribe",
                temperature=0.0,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    threshold=0.5,
                    max_speech_duration_s=30,
                    min_speech_duration_ms=250
                ),
                condition_on_previous_text=False,
                compression_ratio_threshold=2.4,
                log_prob_threshold=-1.0,
                no_speech_threshold=0.6
            )
            
            # 組合所有片段
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())
            text = " ".join(text_parts).strip()
            
            # 過濾明顯錯誤的識別結果
            if len(text) < 2:
                return ""
                
            # 過濾常見誤識別內容
            ignore_phrases = ["謝謝觀看", "請訂閱", "感謝收看", "字幕", "請關注", "點讚"]
            if any(phrase in text for phrase in ignore_phrases):
                return ""
                
            return text
        except Exception as e:
            console.print(f"[red]語音轉錄錯誤: {e}")
            return ""

    async def get_openai_response(self, text: str) -> str:
        """獲取OpenAI GPT-4o-mini回應"""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            console.print(f"[red]OpenAI API錯誤: {e}")
            return "抱歉，OpenAI服務暫時無法回應您的請求。"

    async def get_llm_response(self, text: str) -> str:
        """獲取LLM回應"""
        try:
            session_id = "car_assistant_session"
            
            # 調用對話鏈
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.chain_with_history.invoke(
                    {"input": text},
                    config={"session_id": session_id}
                )
            )
            
            return response.strip()
            
        except Exception as e:
            console.print(f"[red]LLM回應錯誤: {e}")
            return "抱歉，系統暫時無法回應您的請求。"
    
    async def get_dual_response(self, text: str) -> tuple:
        """同時獲取本地ollama和OpenAI的回應"""
        tasks = []
        
        # 添加本地ollama任務
        tasks.append(("Ollama", self.get_llm_response(text)))
        
        # 如果啟用OpenAI，添加OpenAI任務
        if self.use_openai:
            tasks.append(("OpenAI", self.get_openai_response(text)))
        
        # 並行執行所有任務
        results = []
        for name, task in tasks:
            try:
                result = await task
                results.append((name, result))
            except Exception as e:
                results.append((name, f"錯誤: {e}"))
        
        return results

    def continuous_audio_monitoring(self, stop_event):
        """連續音訊監控和VAD檢測 - Windows優化版"""
        self.audio_buffer = []
        silence_start = None
        recording = False
        noise_samples = []
        volume_history = []
        
        def audio_callback(indata, frames, time, status):
            nonlocal recording, silence_start, noise_samples, volume_history
            if status:
                console.print(f"[yellow]音訊狀態: {status}")
            
            # 將音訊數據轉換為numpy數組
            audio_data = np.frombuffer(indata, dtype=np.int16).astype(np.float32) / 32768.0
            
            # 使用音量檢測
            volume = np.sqrt(np.mean(audio_data ** 2))  # RMS音量
            volume_threshold = 0.01  # 回復原始低閾值
            
            if self.vad_model is not None:
                # 使用VAD檢測語音
                try:
                    if volume > volume_threshold and len(audio_data) >= 512:
                        speech_timestamps = get_speech_timestamps(
                            audio_data, 
                            self.vad_model, 
                            sampling_rate=self.sample_rate,
                            threshold=0.3,
                            min_speech_duration_ms=100,
                            min_silence_duration_ms=100
                        )
                        has_speech = len(speech_timestamps) > 0
                    else:
                        has_speech = volume > volume_threshold
                        
                    if has_speech:
                        if not recording:
                            console.print(f"[green]🎤 檢測到語音(音量:{volume:.4f})，開始錄音...")
                            recording = True
                            self.audio_buffer = []
                        self.audio_buffer.extend(audio_data)
                        silence_start = None
                    else:
                        if recording:
                            if silence_start is None:
                                silence_start = time.inputBufferAdcTime
                            elif time.inputBufferAdcTime - silence_start > self.silence_duration:
                                console.print("[blue]🔇 檢測到靜音，停止錄音")
                                recording = False
                                stop_event.set()
                except Exception as e:
                    console.print(f"[yellow]VAD錯誤，使用音量檢測: {e}")
                    # 回退到音量檢測
                    has_speech = volume > volume_threshold
                    if has_speech and not recording:
                        recording = True
                        console.print(f"[yellow]📱 音量檢測模式(音量:{volume:.4f})")
                        self.audio_buffer = []
                    if recording:
                        self.audio_buffer.extend(audio_data)
                        if len(self.audio_buffer) > self.sample_rate * 3:
                            stop_event.set()
            else:
                # 無VAD時使用純音量檢測
                has_speech = volume > volume_threshold
                if has_speech and not recording:
                    recording = True
                    console.print(f"[yellow]📱 音量檢測開始錄音(音量:{volume:.4f})...")
                    self.audio_buffer = []
                if recording:
                    self.audio_buffer.extend(audio_data)
                    if len(self.audio_buffer) > self.sample_rate * 3:
                        stop_event.set()

        # 開始音訊錄製
        with sd.RawInputStream(
            samplerate=self.sample_rate, 
            dtype="int16", 
            channels=1, 
            callback=audio_callback
        ):
            while not stop_event.is_set():
                time.sleep(0.1)

    async def run_assistant(self):
        """運行車載語音助理主循環"""
        console.print("[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        console.print("[cyan]🚗 車載語音助理已啟動")
        console.print("[cyan]🎯 Faster-Whisper 中英文語音識別")
        console.print("[cyan]📝 純文字回覆模式 (無TTS)")
        console.print("[cyan]🎤 系統正在監聽您的語音")
        console.print("[cyan]📱 按Ctrl+C退出系統")
        console.print("[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        try:
            while True:
                console.print("[blue]🔍 VAD 語音偵測中...")
                
                # 開始連續語音監控
                stop_event = threading.Event()
                monitoring_thread = threading.Thread(
                    target=self.continuous_audio_monitoring,
                    args=(stop_event,),
                )
                monitoring_thread.start()
                monitoring_thread.join()
                
                # 當VAD檢測到語音結束時，處理音訊
                audio_np = np.array(self.audio_buffer)
                
                if len(audio_np) > 8000:  # 確保有足夠的音訊數據
                    # 語音轉文字
                    with console.status("🎯 語音識別處理中...", spinner="dots"):
                        text = self.transcribe_chinese(audio_np)
                    
                    if text:
                        console.print(f"[yellow]👤 您說: {text}")
                        
                        # 生成回應
                        if self.use_openai:
                            with console.status("🤖 雙模型助理思考中...", spinner="dots"):
                                responses = await self.get_dual_response(text)
                            
                            # 顯示雙模型回應
                            console.print("[cyan]🤖 助理回應:")
                            for model_name, response in responses:
                                console.print(f"[bold green]{model_name}:[/bold green] {response}")
                                console.print("[dim]─────────────────────────────────────[/dim]")
                        else:
                            with console.status("🤖 助理思考中...", spinner="dots"):
                                response = await self.get_llm_response(text)
                            
                            # 顯示單一模型回應
                            console.print(f"[cyan]🤖 助理: {response}")
                            console.print("[dim]─────────────────────────────────────[/dim]")
                    else:
                        console.print("[red]❌ 未能識別語音，請重試")
                else:
                    console.print("[yellow]⚠️ 音訊太短，請再試一次")
                    
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 正在關閉車載語音助理...")
        except Exception as e:
            console.print(f"[red]❌ 系統錯誤: {e}")

def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(description="車載智慧助理 - 中英文語音識別 + 文字回覆")
    parser.add_argument("--whisper-model", default="medium", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper模型大小 (預設: medium，支援中英文)")
    parser.add_argument("--ollama-model", default="qwen2.5:3b",
                       help="Ollama模型名稱 (預設: qwen2.5:3b)")
    parser.add_argument("--use-openai", action="store_true",
                       help="啟用OpenAI GPT-4o-mini作為第二個回應來源 (需設定 OPENAI_API_KEY 環境變數)")
    
    args = parser.parse_args()
    
    # 創建車載助理實例
    assistant = CarVoiceAssistant(
        whisper_model=args.whisper_model,
        ollama_model=args.ollama_model,
        use_openai=args.use_openai
    )
    
    async def run():
        await assistant.initialize()
        await assistant.run_assistant()
    
    # 運行助理
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        console.print("\n[blue]🚗 車載語音助理已關閉，祝您行車安全！")

if __name__ == "__main__":
    main()