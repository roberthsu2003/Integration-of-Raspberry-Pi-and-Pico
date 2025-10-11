#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料收集系統 - MQTT 訂閱並儲存到 MongoDB
整合 MQTT 訂閱和 FastAPI，自動將感測器資料儲存到資料庫
"""

import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import json
import sys

# ============ 配置參數 ============
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SUBSCRIBE_TOPIC = "sensors/#"

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_readings"

# ============ MongoDB 連接 ============
class DatabaseManager:
    """MongoDB 資料庫管理類別"""
    
    def __init__(self, uri, db_name, collection_name):
        """初始化資料庫連接"""
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"✓ 成功連接到 MongoDB: {db_name}.{collection_name}")
        except Exception as e:
            print(f"✗ MongoDB 連接失敗: {e}")
            sys.exit(1)
    
    def insert_data(self, data):
        """插入資料到資料庫"""
        try:
            # 加入儲存時間戳記
            data['stored_at'] = datetime.now()
            
            # 插入資料
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"✗ 資料插入失敗: {e}")
            return None
    
    def get_stats(self):
        """取得資料庫統計資訊"""
        try:
            count = self.collection.count_documents({})
            return {"total_records": count}
        except Exception as e:
            print(f"✗ 取得統計資訊失敗: {e}")
            return None
    
    def close(self):
        """關閉資料庫連接"""
        self.client.close()

# ============ 資料驗證 ============
def validate_sensor_data(data):
    """驗證感測器資料格式"""
    required_fields = ['device_id', 'sensor_type', 'value']
    
    # 檢查必要欄位
    for field in required_fields:
        if field not in data:
            return False, f"缺少必要欄位: {field}"
    
    # 檢查數值類型
    if not isinstance(data['value'], (int, float)):
        return False, "value 必須是數字"
    
    # 檢查溫度範圍（如果是溫度感測器）
    if data['sensor_type'] == 'temperature':
        if data['value'] < -50 or data['value'] > 100:
            return False, f"溫度值超出合理範圍: {data['value']}"
    
    return True, "驗證通過"

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
    db_manager = userdata['db_manager']
    stats = userdata['stats']
    
    try:
        # 解析 JSON 資料
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        
        # 加入主題資訊
        data['mqtt_topic'] = msg.topic
        
        # 驗證資料
        is_valid, message = validate_sensor_data(data)
        if not is_valid:
            print(f"✗ 資料驗證失敗: {message}")
            print(f"  原始資料: {data}")
            stats['validation_errors'] += 1
            return
        
        # 儲存到資料庫
        doc_id = db_manager.insert_data(data)
        
        if doc_id:
            stats['saved_count'] += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"[{current_time}] ✓ 資料已儲存")
            print(f"  裝置: {data.get('device_id')}")
            print(f"  感測器: {data.get('sensor_type')}")
            print(f"  數值: {data.get('value')} {data.get('unit', '')}")
            print(f"  文件 ID: {doc_id}")
            print(f"  總計: {stats['saved_count']} 筆")
            print("-" * 60)
        else:
            stats['save_errors'] += 1
            
    except json.JSONDecodeError as e:
        print(f"✗ JSON 解析錯誤: {e}")
        stats['parse_errors'] += 1
    except Exception as e:
        print(f"✗ 處理訊息時發生錯誤: {e}")
        stats['other_errors'] += 1

def on_disconnect(client, userdata, rc):
    """當與 MQTT Broker 斷開連接時的回調函式"""
    if rc != 0:
        print(f"\n✗ 意外斷線，錯誤碼: {rc}")

# ============ 主程式 ============
def main():
    """主程式流程"""
    print("=" * 60)
    print("資料收集系統 - MQTT 到 MongoDB")
    print("=" * 60)
    print()
    
    # 初始化資料庫
    db_manager = DatabaseManager(MONGO_URI, MONGO_DB, MONGO_COLLECTION)
    
    # 顯示目前資料庫統計
    stats_info = db_manager.get_stats()
    if stats_info:
        print(f"資料庫現有記錄: {stats_info['total_records']} 筆\n")
    
    # 初始化統計資訊
    stats = {
        'saved_count': 0,
        'validation_errors': 0,
        'save_errors': 0,
        'parse_errors': 0,
        'other_errors': 0
    }
    
    # 建立 MQTT 客戶端
    client = mqtt.Client(client_id="data_collector")
    client.user_data_set({'db_manager': db_manager, 'stats': stats})
    
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
        db_manager.close()
        return
    
    # 開始監聽
    print("\n等待接收資料...")
    print("按 Ctrl+C 停止\n")
    
    try:
        # 開始循環處理訊息
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n程式已停止")
        print("\n統計資訊：")
        print(f"  成功儲存: {stats['saved_count']} 筆")
        print(f"  驗證錯誤: {stats['validation_errors']} 筆")
        print(f"  儲存錯誤: {stats['save_errors']} 筆")
        print(f"  解析錯誤: {stats['parse_errors']} 筆")
        print(f"  其他錯誤: {stats['other_errors']} 筆")
    finally:
        client.disconnect()
        db_manager.close()
        print("\n連接已關閉")

# ============ 執行主程式 ============
if __name__ == "__main__":
    main()
