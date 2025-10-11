#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
裝置管理系統
管理多個 Pico 裝置的註冊、查詢、移除和狀態追蹤
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import json

class DeviceManager:
    """裝置管理類別"""
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="iot_data"):
        """初始化裝置管理器"""
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.devices_collection = self.db['devices']
        self.readings_collection = self.db['sensor_readings']
        
        # 建立索引以提升查詢效能
        self.devices_collection.create_index("device_id", unique=True)
        self.readings_collection.create_index([("device_id", 1), ("stored_at", -1)])
    
    def register_device(self, device_id: str, device_info: Dict) -> bool:
        """
        註冊新裝置
        
        Args:
            device_id: 裝置唯一識別碼
            device_info: 裝置資訊字典
        
        Returns:
            bool: 註冊成功回傳 True
        """
        try:
            device_doc = {
                "device_id": device_id,
                "device_name": device_info.get("device_name", device_id),
                "device_type": device_info.get("device_type", "pico_w"),
                "location": device_info.get("location", "unknown"),
                "sensors": device_info.get("sensors", []),
                "mqtt_topic": device_info.get("mqtt_topic", f"sensors/{device_id}"),
                "status": "registered",
                "registered_at": datetime.now(),
                "last_seen": None,
                "metadata": device_info.get("metadata", {})
            }
            
            self.devices_collection.insert_one(device_doc)
            print(f"✓ 裝置已註冊: {device_id}")
            return True
        except Exception as e:
            print(f"✗ 註冊失敗: {e}")
            return False
    
    def get_device(self, device_id: str) -> Optional[Dict]:
        """取得裝置資訊"""
        device = self.devices_collection.find_one({"device_id": device_id})
        if device:
            device['_id'] = str(device['_id'])
        return device
    
    def get_all_devices(self) -> List[Dict]:
        """取得所有裝置列表"""
        devices = []
        for device in self.devices_collection.find():
            device['_id'] = str(device['_id'])
            devices.append(device)
        return devices
    
    def update_device_status(self, device_id: str, status: str) -> bool:
        """更新裝置狀態"""
        try:
            result = self.devices_collection.update_one(
                {"device_id": device_id},
                {"$set": {
                    "status": status,
                    "last_seen": datetime.now()
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"✗ 更新狀態失敗: {e}")
            return False
    
    def remove_device(self, device_id: str) -> bool:
        """移除裝置"""
        try:
            result = self.devices_collection.delete_one({"device_id": device_id})
            if result.deleted_count > 0:
                print(f"✓ 裝置已移除: {device_id}")
                return True
            else:
                print(f"✗ 找不到裝置: {device_id}")
                return False
        except Exception as e:
            print(f"✗ 移除失敗: {e}")
            return False
    
    def get_device_status(self, device_id: str) -> Dict:
        """取得裝置詳細狀態"""
        device = self.get_device(device_id)
        if not device:
            return {"error": "Device not found"}
        
        # 取得最新讀數
        latest_reading = self.readings_collection.find_one(
            {"device_id": device_id},
            sort=[("stored_at", -1)]
        )
        
        # 計算資料統計
        total_readings = self.readings_collection.count_documents({"device_id": device_id})
        
        # 判斷線上狀態（5分鐘內有資料視為線上）
        is_online = False
        if latest_reading and latest_reading.get('stored_at'):
            time_diff = datetime.now() - latest_reading['stored_at']
            is_online = time_diff < timedelta(minutes=5)
        
        return {
            "device_id": device_id,
            "device_name": device['device_name'],
            "status": "online" if is_online else "offline",
            "last_seen": device.get('last_seen'),
            "total_readings": total_readings,
            "latest_value": latest_reading.get('value') if latest_reading else None,
            "latest_timestamp": latest_reading.get('stored_at') if latest_reading else None
        }
    
    def get_online_devices(self) -> List[str]:
        """取得所有線上裝置"""
        cutoff_time = datetime.now() - timedelta(minutes=5)
        
        # 從讀數中找出最近活躍的裝置
        pipeline = [
            {"$match": {"stored_at": {"$gte": cutoff_time}}},
            {"$group": {"_id": "$device_id"}},
            {"$project": {"device_id": "$_id", "_id": 0}}
        ]
        
        result = self.readings_collection.aggregate(pipeline)
        return [doc['device_id'] for doc in result]
    
    def close(self):
        """關閉資料庫連接"""
        self.client.close()

# ============ CLI 介面 ============
def main():
    """命令列介面"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python device_manager.py register <device_id> <name> <location>")
        print("  python device_manager.py list")
        print("  python device_manager.py status <device_id>")
        print("  python device_manager.py remove <device_id>")
        print("  python device_manager.py online")
        return
    
    manager = DeviceManager()
    command = sys.argv[1]
    
    try:
        if command == "register":
            device_id = sys.argv[2]
            device_name = sys.argv[3] if len(sys.argv) > 3 else device_id
            location = sys.argv[4] if len(sys.argv) > 4 else "unknown"
            
            device_info = {
                "device_name": device_name,
                "location": location,
                "sensors": ["temperature"]
            }
            manager.register_device(device_id, device_info)
        
        elif command == "list":
            devices = manager.get_all_devices()
            print(f"\n找到 {len(devices)} 個裝置:\n")
            for device in devices:
                print(f"  {device['device_id']}")
                print(f"    名稱: {device['device_name']}")
                print(f"    位置: {device['location']}")
                print(f"    狀態: {device['status']}")
                print()
        
        elif command == "status":
            device_id = sys.argv[2]
            status = manager.get_device_status(device_id)
            print(f"\n裝置狀態: {device_id}\n")
            for key, value in status.items():
                print(f"  {key}: {value}")
        
        elif command == "remove":
            device_id = sys.argv[2]
            manager.remove_device(device_id)
        
        elif command == "online":
            online_devices = manager.get_online_devices()
            print(f"\n線上裝置 ({len(online_devices)}):\n")
            for device_id in online_devices:
                print(f"  {device_id}")
        
        else:
            print(f"未知命令: {command}")
    
    finally:
        manager.close()

if __name__ == "__main__":
    main()
