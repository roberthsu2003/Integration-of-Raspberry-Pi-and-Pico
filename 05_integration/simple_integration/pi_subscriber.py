#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pi 簡單整合範例 - MQTT 訂閱者
這個範例展示如何在 Pi 上訂閱 Pico 發布的感測器資料
"""

import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

# ============ 配置參數 ============
MQTT_BROKER = "localhost"  # MQTT Broker 位址
MQTT_PORT = 1883
SUBSCRIBE_TOPIC = "sensors/#"  # 訂閱所有感測器主題

# ============ MQTT 回調函式 ============
def on_connect(client, userdata, flags, rc):
    """當連接到 MQTT Broker 時的回調函式"""
    if rc == 0:
        print(f"✓ 成功連接到 MQTT Broker")
        print(f"✓ 訂閱主題: {SUBSCRIBE_TOPIC}\n")
        client.subscribe(SUBSCRIBE_TOPIC)
    else:
        print(f"✗ 連接失敗，錯誤碼: {rc}")

def on_message(client, userdata, msg):
    """當收到 MQTT 訊息時的回調函式"""
    try:
        # 解析 JSON 資料
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        # 取得當前時間
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 顯示接收到的資料
        print(f"[{current_time}] 收到資料")
        print(f"  主題: {msg.topic}")
        print(f"  裝置: {data.get('device_id', 'unknown')}")
        print(f"  感測器: {data.get('sensor_type', 'unknown')}")
        print(f"  數值: {data.get('value', 'N/A')} {data.get('unit', '')}")
        print("-" * 60)
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON 解析錯誤: {e}")
        print(f"  原始資料: {msg.payload}")
    except Exception as e:
        print(f"✗ 處理訊息時發生錯誤: {e}")

def on_disconnect(client, userdata, rc):
    """當與 MQTT Broker 斷開連接時的回調函式"""
    if rc != 0:
        print(f"\n✗ 意外斷線，錯誤碼: {rc}")
        print("嘗試重新連接...")

# ============ 主程式 ============
def main():
    """主程式流程"""
    print("=" * 60)
    print("Pi 簡單整合範例 - MQTT 訂閱者")
    print("=" * 60)
    print()
    
    # 建立 MQTT 客戶端
    client = mqtt.Client(client_id="pi_subscriber_simple")
    
    # 設定回調函式
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # 連接到 MQTT Broker
    print(f"正在連接到 MQTT Broker: {MQTT_BROKER}:{MQTT_PORT}...")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except Exception as e:
        print(f"✗ 連接失敗: {e}")
        print("\n請確認：")
        print("  1. MQTT Broker (Mosquitto) 已啟動")
        print("  2. MQTT_BROKER 設定正確")
        return
    
    # 開始監聽
    print("\n等待接收資料...")
    print("按 Ctrl+C 停止\n")
    
    try:
        # 開始循環處理訊息
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n程式已停止")
    finally:
        client.disconnect()
        print("MQTT 連接已關閉")

# ============ 執行主程式 ============
if __name__ == "__main__":
    main()
