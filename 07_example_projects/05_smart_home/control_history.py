"""
控制歷史查詢工具
查詢和分析控制命令歷史記錄
"""

import pymongo
import argparse
from datetime import datetime, timedelta
from collections import Counter

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "control_history"

class ControlHistory:
    """控制歷史管理類別"""
    
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.collection = self.client[MONGO_DB][MONGO_COLLECTION]
    
    def list_history(self, device_id=None, hours=24, limit=50):
        """列出控制歷史"""
        query = {}
        
        if device_id:
            query["device_id"] = device_id
        
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            query["timestamp"] = {"$gte": cutoff.isoformat()}
        
        records = list(self.collection.find(
            query,
            {"_id": 0}
        ).sort("timestamp", -1).limit(limit))
        
        return records
    
    def get_statistics(self, device_id=None, hours=24):
        """取得統計資訊"""
        query = {}
        
        if device_id:
            query["device_id"] = device_id
        
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            query["timestamp"] = {"$gte": cutoff.isoformat()}
        
        records = list(self.collection.find(query, {"_id": 0}))
        
        if not records:
            return None
        
        # 統計動作類型
        actions = [r["action"] for r in records]
        action_counts = Counter(actions)
        
        # 統計裝置
        devices = [r["device_id"] for r in records]
        device_counts = Counter(devices)
        
        # 統計規則觸發
        rules = [r.get("rule_name", "manual") for r in records]
        rule_counts = Counter(rules)
        
        return {
            "total_commands": len(records),
            "action_counts": dict(action_counts),
            "device_counts": dict(device_counts),
            "rule_counts": dict(rule_counts),
            "time_range": f"{hours} 小時"
        }
    
    def export_history(self, filename, device_id=None, hours=24):
        """匯出歷史記錄"""
        import json
        
        records = self.list_history(device_id, hours, limit=1000)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        
        return len(records)
    
    def close(self):
        """關閉連接"""
        self.client.close()

def main():
    parser = argparse.ArgumentParser(description="控制歷史查詢工具")
    parser.add_argument("--device", help="裝置 ID")
    parser.add_argument("--hours", type=int, default=24, help="時間範圍（小時）")
    parser.add_argument("--limit", type=int, default=50, help="顯示筆數")
    parser.add_argument("--stats", action="store_true", help="顯示統計資訊")
    parser.add_argument("--export", help="匯出到檔案")
    
    args = parser.parse_args()
    
    history = ControlHistory()
    
    try:
        if args.stats:
            # 顯示統計資訊
            print("=" * 60)
            print("控制歷史統計")
            print("=" * 60)
            
            stats = history.get_statistics(args.device, args.hours)
            
            if stats:
                print(f"\n時間範圍: {stats['time_range']}")
                print(f"總命令數: {stats['total_commands']}")
                
                print("\n動作統計:")
                for action, count in stats['action_counts'].items():
                    print(f"  {action}: {count} 次")
                
                print("\n裝置統計:")
                for device, count in stats['device_counts'].items():
                    print(f"  {device}: {count} 次")
                
                print("\n規則統計:")
                for rule, count in stats['rule_counts'].items():
                    print(f"  {rule}: {count} 次")
            else:
                print("沒有找到記錄")
        
        elif args.export:
            # 匯出記錄
            count = history.export_history(args.export, args.device, args.hours)
            print(f"✓ 已匯出 {count} 筆記錄到 {args.export}")
        
        else:
            # 列出記錄
            print("=" * 60)
            print("控制歷史記錄")
            print("=" * 60)
            
            records = history.list_history(args.device, args.hours, args.limit)
            
            if records:
                for record in records:
                    timestamp = record.get('timestamp', 'N/A')
                    device = record.get('device_id', 'N/A')
                    action = record.get('action', 'N/A')
                    rule = record.get('rule_name', 'manual')
                    
                    print(f"\n時間: {timestamp}")
                    print(f"裝置: {device}")
                    print(f"動作: {action}")
                    print(f"來源: {rule}")
                    print("-" * 60)
                
                print(f"\n共 {len(records)} 筆記錄")
            else:
                print("沒有找到記錄")
    
    finally:
        history.close()

if __name__ == "__main__":
    main()
