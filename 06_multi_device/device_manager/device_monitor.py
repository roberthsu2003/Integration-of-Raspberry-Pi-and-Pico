#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
裝置狀態監控系統
實作心跳檢測、離線警報和狀態追蹤功能
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import List, Dict
import time
import threading

class DeviceMonitor:
    """裝置監控類別"""
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="iot_data",
                 offline_threshold_minutes=5, check_interval_seconds=30):
        """
        初始化裝置監控器
        
        Args:
            mongo_uri: MongoDB 連接字串
            db_name: 資料庫名稱
            offline_threshold_minutes: 離線判定時間（分鐘）
            check_interval_seconds: 檢查間隔（秒）
        """
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.devices_collection = self.db['devices']
        self.readings_collection = self.db['sensor_readings']
        self.alerts_collection = self.db['device_alerts']
        
        self.offline_threshold = timedelta(minutes=offline_threshold_minutes)
        self.check_interval = check_interval_seconds
        self.running = False
        self.monitor_thread = None
        
        # 建立索引
        self.alerts_collection.create_index([("device_id", 1), ("created_at", -1)])
    
    def check_device_heartbeat(self, device_id: str) -> Dict:
        """
        檢查裝置心跳狀態
        
        Args:
            device_id: 裝置 ID
        
        Returns:
            Dict: 包含狀態資訊的字典
        """
        # 取得最新讀數
        latest_reading = self.readings_collection.find_one(
            {"device_id": device_id},
            sort=[("stored_at", -1)]
        )
        
        if not latest_reading:
            return {
                "device_id": device_id,
                "status": "no_data",
                "last_seen": None,
                "time_since_last_seen": None
            }
        
        last_seen = latest_reading.get('stored_at')
        time_diff = datetime.now() - last_seen
        is_online = time_diff < self.offline_threshold
        
        return {
            "device_id": device_id,
            "status": "online" if is_online else "offline",
            "last_seen": last_seen,
            "time_since_last_seen": str(time_diff).split('.')[0]  # 移除微秒
        }
    
    def check_all_devices(self) -> List[Dict]:
        """檢查所有已註冊裝置的狀態"""
        devices = self.devices_collection.find()
        results = []
        
        for device in devices:
            device_id = device['device_id']
            status = self.check_device_heartbeat(device_id)
            results.append(status)
            
            # 更新裝置狀態
            self.devices_collection.update_one(
                {"device_id": device_id},
                {"$set": {
                    "status": status['status'],
                    "last_checked": datetime.now()
                }}
            )
        
        return results
    
    def create_alert(self, device_id: str, alert_type: str, message: str):
        """
        建立裝置警報
        
        Args:
            device_id: 裝置 ID
            alert_type: 警報類型（offline, reconnected, error）
            message: 警報訊息
        """
        alert = {
            "device_id": device_id,
            "alert_type": alert_type,
            "message": message,
            "created_at": datetime.now(),
            "acknowledged": False
        }
        
        self.alerts_collection.insert_one(alert)
        print(f"⚠️  警報: [{device_id}] {message}")
    
    def monitor_loop(self):
        """監控循環"""
        device_states = {}  # 追蹤裝置狀態變化
        
        while self.running:
            try:
                results = self.check_all_devices()
                
                for result in results:
                    device_id = result['device_id']
                    current_status = result['status']
                    previous_status = device_states.get(device_id)
                    
                    # 檢測狀態變化
                    if previous_status != current_status:
                        if current_status == "offline" and previous_status == "online":
                            # 裝置離線
                            self.create_alert(
                                device_id,
                                "offline",
                                f"裝置已離線（最後上線: {result['last_seen']}）"
                            )
                        elif current_status == "online" and previous_status == "offline":
                            # 裝置重新上線
                            self.create_alert(
                                device_id,
                                "reconnected",
                                "裝置已重新上線"
                            )
                    
                    device_states[device_id] = current_status
                
                # 顯示監控狀態
                online_count = sum(1 for r in results if r['status'] == 'online')
                offline_count = sum(1 for r in results if r['status'] == 'offline')
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"線上: {online_count} | 離線: {offline_count}")
                
                time.sleep(self.check_interval)
            
            except Exception as e:
                print(f"✗ 監控錯誤: {e}")
                time.sleep(self.check_interval)
    
    def start_monitoring(self):
        """啟動監控"""
        if self.running:
            print("監控已在執行中")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("✓ 裝置監控已啟動")
    
    def stop_monitoring(self):
        """停止監控"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("✓ 裝置監控已停止")
    
    def get_alerts(self, device_id: str = None, limit: int = 50) -> List[Dict]:
        """
        取得警報記錄
        
        Args:
            device_id: 裝置 ID（可選，不指定則取得所有警報）
            limit: 最多回傳筆數
        
        Returns:
            List[Dict]: 警報列表
        """
        query = {"device_id": device_id} if device_id else {}
        alerts = self.alerts_collection.find(query).sort("created_at", -1).limit(limit)
        
        result = []
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            result.append(alert)
        
        return result
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """確認警報"""
        from bson import ObjectId
        try:
            result = self.alerts_collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": {"acknowledged": True, "acknowledged_at": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"✗ 確認警報失敗: {e}")
            return False
    
    def get_device_statistics(self, device_id: str, hours: int = 24) -> Dict:
        """
        取得裝置統計資訊
        
        Args:
            device_id: 裝置 ID
            hours: 統計時間範圍（小時）
        
        Returns:
            Dict: 統計資訊
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # 計算讀數數量
        total_readings = self.readings_collection.count_documents({
            "device_id": device_id,
            "stored_at": {"$gte": cutoff_time}
        })
        
        # 計算平均值（假設是溫度感測器）
        pipeline = [
            {"$match": {
                "device_id": device_id,
                "stored_at": {"$gte": cutoff_time}
            }},
            {"$group": {
                "_id": None,
                "avg_value": {"$avg": "$value"},
                "min_value": {"$min": "$value"},
                "max_value": {"$max": "$value"}
            }}
        ]
        
        stats = list(self.readings_collection.aggregate(pipeline))
        
        if stats:
            return {
                "device_id": device_id,
                "time_range_hours": hours,
                "total_readings": total_readings,
                "average_value": round(stats[0]['avg_value'], 2) if stats[0]['avg_value'] else None,
                "min_value": stats[0]['min_value'],
                "max_value": stats[0]['max_value']
            }
        else:
            return {
                "device_id": device_id,
                "time_range_hours": hours,
                "total_readings": 0,
                "average_value": None,
                "min_value": None,
                "max_value": None
            }
    
    def close(self):
        """關閉連接"""
        self.stop_monitoring()
        self.client.close()

# ============ CLI 介面 ============
def main():
    """命令列介面"""
    import sys
    
    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python device_monitor.py start              # 啟動監控")
        print("  python device_monitor.py check              # 檢查所有裝置")
        print("  python device_monitor.py alerts [device_id] # 查看警報")
        print("  python device_monitor.py stats <device_id>  # 查看統計")
        return
    
    monitor = DeviceMonitor()
    command = sys.argv[1]
    
    try:
        if command == "start":
            print("裝置狀態監控系統")
            print("=" * 60)
            print(f"離線判定時間: {monitor.offline_threshold}")
            print(f"檢查間隔: {monitor.check_interval} 秒")
            print("按 Ctrl+C 停止監控\n")
            
            monitor.start_monitoring()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n正在停止監控...")
        
        elif command == "check":
            results = monitor.check_all_devices()
            print(f"\n裝置狀態檢查結果 ({len(results)} 個裝置):\n")
            
            for result in results:
                status_icon = "🟢" if result['status'] == 'online' else "🔴"
                print(f"{status_icon} {result['device_id']}")
                print(f"   狀態: {result['status']}")
                if result['last_seen']:
                    print(f"   最後上線: {result['last_seen']}")
                    print(f"   距今: {result['time_since_last_seen']}")
                print()
        
        elif command == "alerts":
            device_id = sys.argv[2] if len(sys.argv) > 2 else None
            alerts = monitor.get_alerts(device_id)
            
            if device_id:
                print(f"\n裝置 {device_id} 的警報記錄 ({len(alerts)} 筆):\n")
            else:
                print(f"\n所有警報記錄 ({len(alerts)} 筆):\n")
            
            for alert in alerts:
                ack_status = "✓" if alert['acknowledged'] else " "
                print(f"[{ack_status}] {alert['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    裝置: {alert['device_id']}")
                print(f"    類型: {alert['alert_type']}")
                print(f"    訊息: {alert['message']}")
                print()
        
        elif command == "stats":
            if len(sys.argv) < 3:
                print("請指定裝置 ID")
                return
            
            device_id = sys.argv[2]
            hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24
            
            stats = monitor.get_device_statistics(device_id, hours)
            print(f"\n裝置統計資訊: {device_id}\n")
            print(f"  時間範圍: 最近 {hours} 小時")
            print(f"  總讀數: {stats['total_readings']}")
            if stats['average_value']:
                print(f"  平均值: {stats['average_value']}")
                print(f"  最小值: {stats['min_value']}")
                print(f"  最大值: {stats['max_value']}")
        
        else:
            print(f"未知命令: {command}")
    
    finally:
        monitor.close()

if __name__ == "__main__":
    main()
