"""
警報歷史查詢工具
"""

import argparse
import json
from datetime import datetime, timedelta
from collections import Counter
import pymongo

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "alerts"

def connect_database():
    """連接到 MongoDB"""
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        print(f"✓ 已連接到 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
        return collection
    except Exception as e:
        print(f"✗ MongoDB 連接失敗: {e}")
        return None

def list_alerts(collection, device_id=None, hours=None, severity=None):
    """列出警報"""
    query = {}
    
    if device_id:
        query["device_id"] = device_id
    
    if severity:
        query["severity"] = severity
    
    if hours:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        query["timestamp"] = {"$gte": cutoff_time.isoformat()}
    
    alerts = list(collection.find(query, {"_id": 0}).sort("timestamp", -1))
    
    if not alerts:
        print("沒有找到警報記錄")
        return
    
    print("\n" + "=" * 80)
    print(f"警報列表 (共 {len(alerts)} 筆)")
    print("=" * 80)
    
    for alert in alerts:
        severity_icon = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'critical': '🚨'
        }.get(alert.get('severity'), '⚠️')
        
        print(f"\n{severity_icon} [{alert.get('severity', 'unknown').upper()}] {alert.get('timestamp')}")
        print(f"  裝置: {alert.get('device_id')}")
        print(f"  規則: {alert.get('rule_name')}")
        print(f"  訊息: {alert.get('message')}")
        if alert.get('value') is not None:
            print(f"  數值: {alert.get('value')}")

def show_statistics(collection, hours=24):
    """顯示警報統計"""
    cutoff_time = datetime.now() - timedelta(hours=hours)
    query = {"timestamp": {"$gte": cutoff_time.isoformat()}}
    
    alerts = list(collection.find(query, {"_id": 0}))
    
    if not alerts:
        print("沒有警報資料")
        return
    
    print("\n" + "=" * 60)
    print(f"警報統計 (最近 {hours} 小時)")
    print("=" * 60)
    
    # 總數
    total = len(alerts)
    print(f"\n總警報數: {total}")
    
    # 按嚴重程度統計
    severity_counts = Counter(a.get('severity') for a in alerts)
    print("\n按嚴重程度:")
    for severity, count in severity_counts.most_common():
        print(f"  - {severity}: {count}")
    
    # 按規則統計
    rule_counts = Counter(a.get('rule_name') for a in alerts)
    print("\n最常觸發的規則:")
    for i, (rule, count) in enumerate(rule_counts.most_common(5), 1):
        print(f"  {i}. {rule}: {count} 次")
    
    # 按裝置統計
    device_counts = Counter(a.get('device_id') for a in alerts)
    print("\n受影響的裝置:")
    for device, count in device_counts.most_common():
        print(f"  - {device}: {count} 次")
    
    print("\n" + "=" * 60)

def export_alerts(collection, output_file, device_id=None, hours=None):
    """匯出警報"""
    query = {}
    
    if device_id:
        query["device_id"] = device_id
    
    if hours:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        query["timestamp"] = {"$gte": cutoff_time.isoformat()}
    
    alerts = list(collection.find(query, {"_id": 0}).sort("timestamp", -1))
    
    if not alerts:
        print("沒有找到警報記錄")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(alerts, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✓ 已匯出 {len(alerts)} 筆警報到 {output_file}")

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description="警報歷史查詢工具")
    
    parser.add_argument("--list", action="store_true", help="列出警報")
    parser.add_argument("--stats", action="store_true", help="顯示統計")
    parser.add_argument("--export", metavar="FILE", help="匯出警報到檔案")
    
    parser.add_argument("--device", help="篩選裝置 ID")
    parser.add_argument("--severity", choices=["info", "warning", "critical"], help="篩選嚴重程度")
    parser.add_argument("--hours", type=int, default=24, help="查詢最近幾小時（預設: 24）")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("警報歷史查詢工具")
    print("=" * 50)
    
    collection = connect_database()
    if not collection:
        return
    
    if args.stats:
        show_statistics(collection, args.hours)
    elif args.export:
        export_alerts(collection, args.export, args.device, args.hours)
    else:
        # 預設列出警報
        list_alerts(collection, args.device, args.hours, args.severity)

if __name__ == "__main__":
    main()
