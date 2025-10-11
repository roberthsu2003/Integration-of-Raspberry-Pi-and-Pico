"""
資料庫管理模組
處理 MongoDB 連接和 CRUD 操作

功能：
- 資料庫連接管理
- 感測器資料的 CRUD 操作
- 裝置資訊管理
- 查詢和篩選
"""

from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
from typing import List, Dict, Optional
import os

class DatabaseManager:
    """
    資料庫管理器類別
    
    負責所有資料庫操作，包括連接、查詢、插入、更新和刪除
    """
    
    def __init__(self, connection_string: str = None):
        """
        初始化資料庫管理器
        
        參數:
            connection_string: MongoDB 連接字串
                             如果未提供，使用環境變數或預設值
        """
        # 取得連接字串
        if connection_string is None:
            connection_string = os.getenv(
                'MONGODB_URL',
                'mongodb://admin:password123@localhost:27017/'
            )
        
        # 資料庫名稱
        self.db_name = os.getenv('MONGO_DATABASE', 'iot_data')
        
        try:
            # 建立 MongoDB 客戶端
            self.client = MongoClient(connection_string)
            
            # 選擇資料庫
            self.db = self.client[self.db_name]
            
            # 取得集合（Collection）
            self.sensor_data = self.db['sensor_data']
            self.devices = self.db['devices']
            
            print(f"✓ 成功連接到 MongoDB 資料庫: {self.db_name}")
            
        except ConnectionFailure as e:
            print(f"✗ MongoDB 連接失敗: {e}")
            raise
    
    def check_connection(self) -> bool:
        """
        檢查資料庫連接狀態
        
        返回:
            bool: True 表示連接正常，False 表示連接失敗
        """
        try:
            # 執行 ping 命令測試連接
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"資料庫連接檢查失敗: {e}")
            return False
    
    def close(self):
        """關閉資料庫連接"""
        if self.client:
            self.client.close()
            print("資料庫連接已關閉")
    
    # ========================================================================
    # 感測器資料操作
    # ========================================================================
    
    def insert_sensor_data(self, data: dict) -> str:
        """
        插入感測器資料
        
        參數:
            data: 感測器資料字典
        
        返回:
            str: 插入資料的 ID
        """
        try:
            # 確保有時間戳記
            if 'timestamp' not in data:
                data['timestamp'] = datetime.now()
            
            # 插入資料
            result = self.sensor_data.insert_one(data)
            
            print(f"✓ 插入感測器資料: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            print(f"✗ 插入感測器資料失敗: {e}")
            raise
    
    def query_sensor_data(
        self,
        filter_dict: dict = None,
        limit: int = 100,
        skip: int = 0,
        sort_by: str = 'timestamp',
        sort_order: int = DESCENDING
    ) -> List[dict]:
        """
        查詢感測器資料
        
        參數:
            filter_dict: 查詢過濾條件
            limit: 返回資料筆數上限
            skip: 跳過的資料筆數（用於分頁）
            sort_by: 排序欄位
            sort_order: 排序順序（DESCENDING 或 ASCENDING）
        
        返回:
            List[dict]: 感測器資料列表
        """
        try:
            if filter_dict is None:
                filter_dict = {}
            
            # 查詢資料
            cursor = self.sensor_data.find(filter_dict) \
                                     .sort(sort_by, sort_order) \
                                     .skip(skip) \
                                     .limit(limit)
            
            # 轉換為列表並處理 ObjectId
            data = []
            for doc in cursor:
                # 將 ObjectId 轉換為字串
                doc['_id'] = str(doc['_id'])
                # 將 datetime 轉換為 ISO 格式字串
                if 'timestamp' in doc and isinstance(doc['timestamp'], datetime):
                    doc['timestamp'] = doc['timestamp'].isoformat()
                data.append(doc)
            
            return data
            
        except Exception as e:
            print(f"✗ 查詢感測器資料失敗: {e}")
            raise
    
    def get_device_data(
        self,
        device_id: str,
        limit: int = 100,
        skip: int = 0
    ) -> List[dict]:
        """
        查詢特定裝置的感測器資料
        
        參數:
            device_id: 裝置 ID
            limit: 返回資料筆數上限
            skip: 跳過的資料筆數
        
        返回:
            List[dict]: 該裝置的感測器資料列表
        """
        filter_dict = {'device_id': device_id}
        return self.query_sensor_data(filter_dict, limit=limit, skip=skip)
    
    def get_latest_data(self, device_id: str = None) -> dict:
        """
        取得最新的感測器資料
        
        參數:
            device_id: 裝置 ID（選用）
        
        返回:
            dict: 最新的感測器資料
        """
        try:
            filter_dict = {}
            if device_id:
                filter_dict['device_id'] = device_id
            
            # 查詢最新一筆資料
            doc = self.sensor_data.find_one(
                filter_dict,
                sort=[('timestamp', DESCENDING)]
            )
            
            if doc:
                doc['_id'] = str(doc['_id'])
                if 'timestamp' in doc and isinstance(doc['timestamp'], datetime):
                    doc['timestamp'] = doc['timestamp'].isoformat()
            
            return doc
            
        except Exception as e:
            print(f"✗ 取得最新資料失敗: {e}")
            raise
    
    def delete_device_data(self, device_id: str) -> int:
        """
        刪除特定裝置的所有資料
        
        參數:
            device_id: 裝置 ID
        
        返回:
            int: 刪除的資料筆數
        """
        try:
            result = self.sensor_data.delete_many({'device_id': device_id})
            print(f"✓ 刪除 {result.deleted_count} 筆資料（裝置: {device_id}）")
            return result.deleted_count
            
        except Exception as e:
            print(f"✗ 刪除資料失敗: {e}")
            raise
    
    def get_data_count(self, filter_dict: dict = None) -> int:
        """
        取得資料筆數
        
        參數:
            filter_dict: 查詢過濾條件
        
        返回:
            int: 資料筆數
        """
        try:
            if filter_dict is None:
                filter_dict = {}
            
            count = self.sensor_data.count_documents(filter_dict)
            return count
            
        except Exception as e:
            print(f"✗ 取得資料筆數失敗: {e}")
            raise
    
    # ========================================================================
    # 裝置管理操作
    # ========================================================================
    
    def register_device(self, device_info: dict) -> str:
        """
        註冊新裝置
        
        參數:
            device_info: 裝置資訊字典
        
        返回:
            str: 插入資料的 ID
        """
        try:
            # 檢查裝置是否已存在
            existing = self.devices.find_one({'device_id': device_info['device_id']})
            
            if existing:
                # 更新現有裝置
                self.devices.update_one(
                    {'device_id': device_info['device_id']},
                    {'$set': {
                        **device_info,
                        'last_seen': datetime.now()
                    }}
                )
                print(f"✓ 更新裝置資訊: {device_info['device_id']}")
                return str(existing['_id'])
            else:
                # 插入新裝置
                device_info['created_at'] = datetime.now()
                device_info['last_seen'] = datetime.now()
                result = self.devices.insert_one(device_info)
                print(f"✓ 註冊新裝置: {device_info['device_id']}")
                return str(result.inserted_id)
            
        except Exception as e:
            print(f"✗ 註冊裝置失敗: {e}")
            raise
    
    def get_device(self, device_id: str) -> dict:
        """
        查詢特定裝置資訊
        
        參數:
            device_id: 裝置 ID
        
        返回:
            dict: 裝置資訊
        """
        try:
            doc = self.devices.find_one({'device_id': device_id})
            
            if doc:
                doc['_id'] = str(doc['_id'])
                # 轉換 datetime 為 ISO 格式
                for key in ['created_at', 'last_seen']:
                    if key in doc and isinstance(doc[key], datetime):
                        doc[key] = doc[key].isoformat()
            
            return doc
            
        except Exception as e:
            print(f"✗ 查詢裝置失敗: {e}")
            raise
    
    def get_all_devices(self) -> List[dict]:
        """
        查詢所有裝置
        
        返回:
            List[dict]: 裝置列表
        """
        try:
            cursor = self.devices.find()
            
            devices = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                # 轉換 datetime 為 ISO 格式
                for key in ['created_at', 'last_seen']:
                    if key in doc and isinstance(doc[key], datetime):
                        doc[key] = doc[key].isoformat()
                devices.append(doc)
            
            return devices
            
        except Exception as e:
            print(f"✗ 查詢所有裝置失敗: {e}")
            raise
    
    def update_device_status(self, device_id: str, status: str) -> bool:
        """
        更新裝置狀態
        
        參數:
            device_id: 裝置 ID
            status: 新狀態
        
        返回:
            bool: 更新是否成功
        """
        try:
            result = self.devices.update_one(
                {'device_id': device_id},
                {'$set': {
                    'status': status,
                    'last_seen': datetime.now()
                }}
            )
            
            if result.modified_count > 0:
                print(f"✓ 更新裝置狀態: {device_id} -> {status}")
                return True
            else:
                print(f"✗ 裝置不存在或狀態未變更: {device_id}")
                return False
            
        except Exception as e:
            print(f"✗ 更新裝置狀態失敗: {e}")
            raise
    
    def delete_device(self, device_id: str) -> bool:
        """
        刪除裝置
        
        參數:
            device_id: 裝置 ID
        
        返回:
            bool: 刪除是否成功
        """
        try:
            result = self.devices.delete_one({'device_id': device_id})
            
            if result.deleted_count > 0:
                print(f"✓ 刪除裝置: {device_id}")
                return True
            else:
                print(f"✗ 裝置不存在: {device_id}")
                return False
            
        except Exception as e:
            print(f"✗ 刪除裝置失敗: {e}")
            raise
    
    # ========================================================================
    # 統計和分析
    # ========================================================================
    
    def get_device_statistics(self, device_id: str) -> dict:
        """
        取得裝置的統計資料
        
        參數:
            device_id: 裝置 ID
        
        返回:
            dict: 統計資料（平均值、最大值、最小值等）
        """
        try:
            pipeline = [
                {'$match': {'device_id': device_id}},
                {'$group': {
                    '_id': '$device_id',
                    'count': {'$sum': 1},
                    'avg_value': {'$avg': '$value'},
                    'min_value': {'$min': '$value'},
                    'max_value': {'$max': '$value'},
                    'latest_timestamp': {'$max': '$timestamp'}
                }}
            ]
            
            result = list(self.sensor_data.aggregate(pipeline))
            
            if result:
                stats = result[0]
                # 轉換 datetime 為 ISO 格式
                if 'latest_timestamp' in stats and isinstance(stats['latest_timestamp'], datetime):
                    stats['latest_timestamp'] = stats['latest_timestamp'].isoformat()
                return stats
            else:
                return {}
            
        except Exception as e:
            print(f"✗ 取得統計資料失敗: {e}")
            raise

# ============================================================================
# 使用範例
# ============================================================================

if __name__ == "__main__":
    # 建立資料庫管理器
    db = DatabaseManager()
    
    # 測試連接
    if db.check_connection():
        print("資料庫連接測試成功！")
        
        # 插入測試資料
        test_data = {
            'device_id': 'pico_test',
            'device_type': 'pico_w',
            'sensor_type': 'temperature',
            'value': 25.5,
            'unit': 'celsius',
            'location': 'test_lab'
        }
        
        data_id = db.insert_sensor_data(test_data)
        print(f"插入測試資料 ID: {data_id}")
        
        # 查詢資料
        data = db.get_device_data('pico_test', limit=5)
        print(f"查詢到 {len(data)} 筆資料")
        
        # 取得統計資料
        stats = db.get_device_statistics('pico_test')
        print(f"統計資料: {stats}")
        
        # 關閉連接
        db.close()
    else:
        print("資料庫連接測試失敗！")
