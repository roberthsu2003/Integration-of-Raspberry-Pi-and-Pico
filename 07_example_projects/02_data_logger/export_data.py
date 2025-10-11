"""
資料匯出工具
支援 JSON 和 CSV 格式匯出
"""

import argparse
import json
import csv
from datetime import datetime, timedelta
import pymongo

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_logs"

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

def build_query(args):
    """建立查詢條件"""
    query = {}
    
    # 裝置篩選
    if args.device:
        query["device_id"] = args.device
    
    # 感測器類型篩選
    if args.sensor_type:
        query["sensor_type"] = args.sensor_type
    
    # 時間範圍篩選
    if args.start or args.end or args.days:
        time_query = {}
        
        if args.days:
            # 最近 N 天
            start_time = datetime.now() - timedelta(days=args.days)
            time_query["$gte"] = start_time.isoformat()
        else:
            if args.start:
                time_query["$gte"] = args.start
            if args.end:
                time_query["$lte"] = args.end
        
        if time_query:
            query["timestamp"] = time_query
    
    return query

def export_json(collection, query, output_file):
    """匯出為 JSON 格式"""
    try:
        print(f"正在查詢資料...")
        data = list(collection.find(query, {"_id": 0}).sort("timestamp", 1))
        
        print(f"找到 {len(data)} 筆資料")
        
        if len(data) == 0:
            print("⚠️  沒有符合條件的資料")
            return False
        
        print(f"正在寫入檔案: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✓ 成功匯出 {len(data)} 筆資料到 {output_file}")
        return True
    except Exception as e:
        print(f"✗ 匯出失敗: {e}")
        return False

def export_csv(collection, query, output_file):
    """匯出為 CSV 格式"""
    try:
        print(f"正在查詢資料...")
        data = list(collection.find(query, {"_id": 0}).sort("timestamp", 1))
        
        print(f"找到 {len(data)} 筆資料")
        
        if len(data) == 0:
            print("⚠️  沒有符合條件的資料")
            return False
        
        # 取得所有欄位名稱
        fieldnames = set()
        for record in data:
            fieldnames.update(record.keys())
        fieldnames = sorted(fieldnames)
        
        print(f"正在寫入檔案: {output_file}")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✓ 成功匯出 {len(data)} 筆資料到 {output_file}")
        return True
    except Exception as e:
        print(f"✗ 匯出失敗: {e}")
        return False

def print_summary(collection, query):
    """印出資料摘要"""
    try:
        count = collection.count_documents(query)
        print("\n" + "=" * 50)
        print("資料摘要")
        print("=" * 50)
        print(f"符合條件的資料筆數: {count}")
        
        if count > 0:
            # 取得時間範圍
            first = collection.find_one(query, sort=[("timestamp", 1)])
            last = collection.find_one(query, sort=[("timestamp", -1)])
            
            if first and last:
                print(f"時間範圍: {first['timestamp']} 到 {last['timestamp']}")
            
            # 取得裝置列表
            devices = collection.distinct("device_id", query)
            print(f"裝置數量: {len(devices)}")
            print(f"裝置列表: {', '.join(devices)}")
        
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"⚠️  無法取得摘要: {e}")

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description="資料匯出工具")
    
    # 匯出格式
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="匯出格式 (預設: json)"
    )
    
    # 輸出檔案
    parser.add_argument(
        "--output",
        required=True,
        help="輸出檔案名稱"
    )
    
    # 篩選條件
    parser.add_argument("--device", help="裝置 ID")
    parser.add_argument("--sensor-type", help="感測器類型")
    parser.add_argument("--start", help="開始時間 (ISO 格式)")
    parser.add_argument("--end", help="結束時間 (ISO 格式)")
    parser.add_argument("--days", type=int, help="最近 N 天")
    
    # 其他選項
    parser.add_argument("--summary", action="store_true", help="顯示資料摘要")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("資料匯出工具")
    print("=" * 50)
    
    # 連接資料庫
    collection = connect_database()
    if not collection:
        return
    
    # 建立查詢條件
    query = build_query(args)
    print(f"查詢條件: {query if query else '全部資料'}")
    
    # 顯示摘要
    if args.summary:
        print_summary(collection, query)
    
    # 匯出資料
    if args.format == "json":
        export_json(collection, query, args.output)
    elif args.format == "csv":
        export_csv(collection, query, args.output)

if __name__ == "__main__":
    main()
