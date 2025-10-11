"""
資料庫管理模組
"""

from pymongo import MongoClient, DESCENDING
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """MongoDB 資料庫管理類別"""
    
    def __init__(self, uri: str, database_name: str):
        """
        初始化資料庫管理器
        
        Args:
            uri: MongoDB 連接字串
            database_name: 資料庫名稱
        """
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None
    
    def connect(self):
        """連接到 MongoDB"""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            self.collection = self.db["sensor_data"]
            
            # 測試連接
            self.client.server_info()
            print(f"✓ 已連接到 MongoDB: {self.database_name}")
            
            # 建立索引
            self.collection.create_index([("device_id", 1)])
            self.collection.create_index([("timestamp", DESCENDING)])
            
        except Exception as e:
            print(f"✗ MongoDB 連接失敗: {e}")
            raise
    
    def disconnect(self):
        """斷開資料庫連接"""
        if self.client:
            self.client.close()
            print("MongoDB 連接已關閉")
    
    def insert_sensor_data(self, data: Dict[str, Any]) -> str:
        """
        插入感測器資料
        
        Args:
            data: 感測器資料字典
            
        Returns:
            str: 插入資料的 ID
        """
        try:
            # 加入儲存時間
            data["saved_at"] = datetime.now()
            
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"插入資料失敗: {e}")
            raise
    
    def get_all_data(self, limit: int = 100) -> List[Dict]:
        """
        取得所有資料
        
        Args:
            limit: 回傳資料筆數限制
            
        Returns:
            List[Dict]: 資料列表
        """
        try:
            cursor = self.collection.find().sort("timestamp", DESCENDING).limit(limit)
            data = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])  # 轉換 ObjectId 為字串
                data.append(doc)
            return data
        except Exception as e:
            print(f"查詢資料失敗: {e}")
            raise
    
    def get_device_data(self, device_id: str, limit: int = 50) -> List[Dict]:
        """
        取得特定裝置的資料
        
        Args:
            device_id: 裝置 ID
            limit: 回傳資料筆數限制
            
        Returns:
            List[Dict]: 資料列表
        """
        try:
            cursor = self.collection.find(
                {"device_id": device_id}
            ).sort("timestamp", DESCENDING).limit(limit)
            
            data = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                data.append(doc)
            return data
        except Exception as e:
            print(f"查詢裝置資料失敗: {e}")
            raise
    
    def get_device_list(self) -> List[Dict]:
        """
        取得所有裝置列表
        
        Returns:
            List[Dict]: 裝置資訊列表
        """
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$device_id",
                        "last_seen": {"$max": "$timestamp"},
                        "data_count": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "device_id": "$_id",
                        "last_seen": 1,
                        "data_count": 1,
                        "_id": 0
                    }
                }
            ]
            
            devices = list(self.collection.aggregate(pipeline))
            return devices
        except Exception as e:
            print(f"查詢裝置列表失敗: {e}")
            raise
    
    def clear_all_data(self) -> int:
        """
        清除所有資料
        
        Returns:
            int: 刪除的資料筆數
        """
        try:
            result = self.collection.delete_many({})
            return result.deleted_count
        except Exception as e:
            print(f"清除資料失敗: {e}")
            raise
    
    def get_latest_data(self, device_id: str) -> Optional[Dict]:
        """
        取得裝置的最新資料
        
        Args:
            device_id: 裝置 ID
            
        Returns:
            Optional[Dict]: 最新資料，如果沒有則回傳 None
        """
        try:
            doc = self.collection.find_one(
                {"device_id": device_id},
                sort=[("timestamp", DESCENDING)]
            )
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception as e:
            print(f"查詢最新資料失敗: {e}")
            raise
