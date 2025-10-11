"""
手動控制工具
透過 MQTT 發送控制命令
"""

import argparse
import json
from datetime import datetime
import paho.mqtt.publish as publish
import pymongo

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

ACTIONS = ["led_on", "led_off", "fan_on", "fan_off", "heater_on", "heater_off", "all_off"]

def save_to_history(device_id, action):
    """儲存到歷史記錄"""
    try:
        client = pymongo.MongoClient("mongodb://admin:password123@localhost:27017/")
        collection = client["iot_data"]["control_history"]
        
        collection.insert_one({
            "device_id": device_id,
            "action": action,
            "rule_name": "manual",
            "timestamp": datetime.now().isoformat()
        })
        
        client.close()
    except Exception as e:
        print(f"⚠ 記錄歷史失敗: {e}")

def send_command(device_id, action):
    """發送控制命令"""
    topic = f"control/{device_id}"
    command = {"action": action, "timestamp": datetime.now().isoformat()}
    
    try:
        publish.single(topic, json.dumps(command), hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"✓ 已發送命令: {device_id} -> {action}")
        
        # 記錄到歷史
        save_to_history(device_id, action)
        
        return True
    except Exception as e:
        print(f"✗ 發送失敗: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="手動控制工具")
    parser.add_argument("--device", required=True, help="裝置 ID")
    parser.add_argument("--action", required=True, choices=ACTIONS, help="控制動作")
    
    args = parser.parse_args()
    
    print("=" * 40)
    print("手動控制工具")
    print("=" * 40)
    print(f"裝置: {args.device}")
    print(f"動作: {args.action}")
    print("-" * 40)
    
    send_command(args.device, args.action)

if __name__ == "__main__":
    main()
