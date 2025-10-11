"""
手動控制工具
透過 MQTT 發送控制命令
"""

import argparse
import json
import paho.mqtt.publish as publish

MQTT_BROKER = "localhost"
MQTT_PORT = 1883

ACTIONS = ["led_on", "led_off", "fan_on", "fan_off", "heater_on", "heater_off", "all_off"]

def send_command(device_id, action):
    """發送控制命令"""
    topic = f"control/{device_id}"
    command = {"action": action}
    
    try:
        publish.single(topic, json.dumps(command), hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"✓ 已發送命令: {device_id} -> {action}")
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
