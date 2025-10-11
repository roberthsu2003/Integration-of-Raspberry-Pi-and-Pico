"""
備份管理工具
支援資料備份和還原功能
"""

import argparse
import json
import os
from datetime import datetime
import pymongo

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_logs"

# 備份目錄
BACKUP_DIR = "backups"

def ensure_backup_dir():
    """確保備份目錄存在"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✓ 已建立備份目錄: {BACKUP_DIR}")

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

def create_backup(collection, output_file=None):
    """建立備份"""
    try:
        ensure_backup_dir()
        
        # 如果沒有指定檔案名稱，使用時間戳記
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")
        
        print(f"正在備份資料...")
        
        # 查詢所有資料
        data = list(collection.find({}, {"_id": 0}))
        count = len(data)
        
        print(f"找到 {count} 筆資料")
        
        # 寫入備份檔案
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "backup_time": datetime.now().isoformat(),
                "record_count": count,
                "data": data
            }, f, indent=2, ensure_ascii=False, default=str)
        
        # 取得檔案大小
        file_size = os.path.getsize(output_file)
        size_mb = file_size / (1024 * 1024)
        
        print(f"✓ 備份完成")
        print(f"  檔案: {output_file}")
        print(f"  筆數: {count}")
        print(f"  大小: {size_mb:.2f} MB")
        
        return True
    except Exception as e:
        print(f"✗ 備份失敗: {e}")
        return False

def restore_backup(collection, backup_file):
    """還原備份"""
    try:
        if not os.path.exists(backup_file):
            print(f"✗ 備份檔案不存在: {backup_file}")
            return False
        
        print(f"正在讀取備份檔案: {backup_file}")
        
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        data = backup_data.get("data", [])
        count = len(data)
        
        print(f"備份時間: {backup_data.get('backup_time', 'Unknown')}")
        print(f"資料筆數: {count}")
        
        # 確認還原
        response = input(f"\n⚠️  這將會清除現有資料並還原 {count} 筆資料。確定要繼續嗎？ (yes/no): ")
        if response.lower() != 'yes':
            print("已取消還原")
            return False
        
        print("正在清除現有資料...")
        result = collection.delete_many({})
        print(f"已刪除 {result.deleted_count} 筆資料")
        
        print("正在還原資料...")
        if count > 0:
            collection.insert_many(data)
        
        print(f"✓ 還原完成，已還原 {count} 筆資料")
        return True
    except Exception as e:
        print(f"✗ 還原失敗: {e}")
        return False

def list_backups():
    """列出所有備份檔案"""
    try:
        ensure_backup_dir()
        
        files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.json')]
        
        if not files:
            print("沒有找到備份檔案")
            return
        
        print("\n" + "=" * 70)
        print("備份檔案列表")
        print("=" * 70)
        
        files.sort(reverse=True)
        
        for filename in files:
            filepath = os.path.join(BACKUP_DIR, filename)
            file_size = os.path.getsize(filepath)
            size_mb = file_size / (1024 * 1024)
            
            # 讀取備份資訊
            try:
                with open(filepath, 'r') as f:
                    backup_data = json.load(f)
                    backup_time = backup_data.get('backup_time', 'Unknown')
                    record_count = backup_data.get('record_count', 0)
                
                print(f"\n檔案: {filename}")
                print(f"  時間: {backup_time}")
                print(f"  筆數: {record_count}")
                print(f"  大小: {size_mb:.2f} MB")
            except:
                print(f"\n檔案: {filename}")
                print(f"  大小: {size_mb:.2f} MB")
                print(f"  (無法讀取備份資訊)")
        
        print("\n" + "=" * 70)
    except Exception as e:
        print(f"✗ 列出備份失敗: {e}")

def main():
    """主程式"""
    parser = argparse.ArgumentParser(description="備份管理工具")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--backup", action="store_true", help="建立備份")
    group.add_argument("--restore", metavar="FILE", help="還原備份")
    group.add_argument("--list", action="store_true", help="列出所有備份")
    
    parser.add_argument("--output", help="備份檔案名稱（選填）")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("備份管理工具")
    print("=" * 50)
    
    if args.list:
        list_backups()
        return
    
    # 連接資料庫
    collection = connect_database()
    if not collection:
        return
    
    if args.backup:
        create_backup(collection, args.output)
    elif args.restore:
        restore_backup(collection, args.restore)

if __name__ == "__main__":
    main()
