#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多裝置 MQTT 訂閱器 - 支援多個主題和裝置識別"""

import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "iot_data"

class MultiDeviceSubscriber:
    def __init__(self):
        self.mongo_client = MongoClient(MONGO_URI)
        self.db = self.mongo_client[MONGO_DB]
        self.collection = self.db['sensor_readings']
        self.devices_collection = self.db['devices']
        self.stats = {}
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✓ 已連接 MQTT Broker")
            # 訂閱所有感測器主題
            client.subscribe("sensors/#")
            print("✓ 訂閱主題: sensors/#\n")
    
    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            device_id = data.get('device_id')
            
            # 更新裝置最後上線時間
            self.devices_collection.update_one(
                {"device_id": device_id},
                {"$set": {"last_seen": datetime.now(), "status": "online"}},
                upsert=True
            )
            
            # 儲存資料
            data['mqtt_topic'] = msg.topic
            data['stored_at'] = datetime.now()
            self.collection.insert_one(data)
            
            # 更新統計
            if device_id not in self.stats:
                self.stats[device_id] = 0
            self.stats[device_id] += 1
            
            print(f"[{device_id}] {data.get('value')} {data.get('unit')} (總計: {self.stats[device_id]})")
        except Exception as e:
            print(f"✗ 錯誤: {e}")
    
    def run(self):
        client = mqtt.Client(client_id="multi_device_subscriber")
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        
        print("多裝置 MQTT 訂閱器")
        print("=" * 60)
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\n\n統計資訊:")
            for device_id, count in self.stats.items():
                print(f"  {device_id}: {count} 筆")
        finally:
            client.disconnect()
            self.mongo_client.close()

if __name__ == "__main__":
    subscriber = MultiDeviceSubscriber()
    subscriber.run()
