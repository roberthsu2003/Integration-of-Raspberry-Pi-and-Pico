#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
資料查詢 API 服務
提供 RESTful API 端點查詢儲存在 MongoDB 的感測器資料
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
import uvicorn

# ============ 配置參數 ============
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_readings"

# ============ 資料模型 ============
class SensorReading(BaseModel):
    """感測器讀數資料模型"""
    device_id: str
    device_type: Optional[str] = None
    sensor_type: str
    value: float
    unit: Optional[str] = None
    timestamp: Optional[float] = None
    mqtt_topic: Optional[str] = None
    stored_at: Optional[datetime] = None

class QueryResponse(BaseModel):
    """查詢回應模型"""
    status: str
    count: int
    data: List[dict]
    message: Optional[str] = None

class StatsResponse(BaseModel):
    """統計資訊回應模型"""
    status: str
    device_id: str
    total_records: int
    avg_value: Optional[float] = None
    max_value: Optional[float] = None
    min_value: Optional[float] = None
    first_reading: Optional[datetime] = None
    last_reading: Optional[datetime] = None

# ============ FastAPI 應用程式 ============
app = FastAPI(
    title="IoT 資料查詢 API",
    description="查詢 Pico 感測器資料的 RESTful API",
    version="1.0.0"
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ 資料庫連接 ============
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    print(f"✓ 成功連接到 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
except Exception as e:
    print(f"✗ MongoDB 連接失敗: {e}")
    mongo_client = None

# ============ API 端點 ============

@app.get("/")
async def root():
    """根端點 - API 資訊"""
    return {
        "name": "IoT 資料查詢 API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "all_data": "/api/data",
            "device_data": "/api/data/{device_id}",
            "time_range": "/api/data/range",
            "statistics": "/api/stats/{device_id}",
            "devices": "/api/devices"
        }
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    if mongo_client is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        # 測試資料庫連接
        mongo_client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.get("/api/data", response_model=QueryResponse)
async def get_all_data(
    limit: int = Query(default=100, ge=1, le=1000, description="最多回傳筆數"),
    skip: int = Query(default=0, ge=0, description="跳過筆數（分頁用）")
):
    """取得所有感測器資料（分頁）"""
    try:
        # 查詢資料，按儲存時間降序排列
        cursor = collection.find().sort("stored_at", -1).skip(skip).limit(limit)
        data = []
        
        for doc in cursor:
            # 轉換 ObjectId 為字串
            doc['_id'] = str(doc['_id'])
            # 轉換 datetime 為 ISO 格式字串
            if 'stored_at' in doc and isinstance(doc['stored_at'], datetime):
                doc['stored_at'] = doc['stored_at'].isoformat()
            data.append(doc)
        
        return QueryResponse(
            status="success",
            count=len(data),
            data=data,
            message=f"成功取得 {len(data)} 筆資料"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗: {str(e)}")

@app.get("/api/data/{device_id}", response_model=QueryResponse)
async def get_device_data(
    device_id: str,
    limit: int = Query(default=100, ge=1, le=1000, description="最多回傳筆數")
):
    """取得特定裝置的感測器資料"""
    try:
        # 查詢特定裝置的資料
        cursor = collection.find({"device_id": device_id}).sort("stored_at", -1).limit(limit)
        data = []
        
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if 'stored_at' in doc and isinstance(doc['stored_at'], datetime):
                doc['stored_at'] = doc['stored_at'].isoformat()
            data.append(doc)
        
        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"找不到裝置 {device_id} 的資料"
            )
        
        return QueryResponse(
            status="success",
            count=len(data),
            data=data,
            message=f"成功取得裝置 {device_id} 的 {len(data)} 筆資料"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗: {str(e)}")

@app.get("/api/data/range", response_model=QueryResponse)
async def get_data_by_time_range(
    device_id: Optional[str] = Query(default=None, description="裝置 ID（選填）"),
    start_time: Optional[str] = Query(default=None, description="開始時間 (ISO 格式)"),
    end_time: Optional[str] = Query(default=None, description="結束時間 (ISO 格式)"),
    hours: Optional[int] = Query(default=None, ge=1, le=168, description="最近 N 小時"),
    limit: int = Query(default=1000, ge=1, le=10000, description="最多回傳筆數")
):
    """依時間範圍查詢資料"""
    try:
        # 建立查詢條件
        query = {}
        
        # 裝置 ID 過濾
        if device_id:
            query["device_id"] = device_id
        
        # 時間範圍過濾
        time_filter = {}
        
        if hours:
            # 使用相對時間（最近 N 小時）
            cutoff_time = datetime.now() - timedelta(hours=hours)
            time_filter["$gte"] = cutoff_time
        else:
            # 使用絕對時間
            if start_time:
                time_filter["$gte"] = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            if end_time:
                time_filter["$lte"] = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        if time_filter:
            query["stored_at"] = time_filter
        
        # 執行查詢
        cursor = collection.find(query).sort("stored_at", -1).limit(limit)
        data = []
        
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            if 'stored_at' in doc and isinstance(doc['stored_at'], datetime):
                doc['stored_at'] = doc['stored_at'].isoformat()
            data.append(doc)
        
        return QueryResponse(
            status="success",
            count=len(data),
            data=data,
            message=f"成功取得 {len(data)} 筆資料"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"時間格式錯誤: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗: {str(e)}")

@app.get("/api/stats/{device_id}", response_model=StatsResponse)
async def get_device_statistics(device_id: str):
    """取得特定裝置的統計資訊"""
    try:
        # 使用 MongoDB aggregation 計算統計
        pipeline = [
            {"$match": {"device_id": device_id}},
            {"$group": {
                "_id": "$device_id",
                "total_records": {"$sum": 1},
                "avg_value": {"$avg": "$value"},
                "max_value": {"$max": "$value"},
                "min_value": {"$min": "$value"},
                "first_reading": {"$min": "$stored_at"},
                "last_reading": {"$max": "$stored_at"}
            }}
        ]
        
        result = list(collection.aggregate(pipeline))
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"找不到裝置 {device_id} 的資料"
            )
        
        stats = result[0]
        
        return StatsResponse(
            status="success",
            device_id=device_id,
            total_records=stats['total_records'],
            avg_value=round(stats['avg_value'], 2) if stats['avg_value'] else None,
            max_value=stats['max_value'],
            min_value=stats['min_value'],
            first_reading=stats['first_reading'],
            last_reading=stats['last_reading']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"統計計算失敗: {str(e)}")

@app.get("/api/devices")
async def get_all_devices():
    """取得所有裝置列表"""
    try:
        # 取得所有不重複的裝置 ID
        device_ids = collection.distinct("device_id")
        
        # 取得每個裝置的最新資料
        devices = []
        for device_id in device_ids:
            latest = collection.find_one(
                {"device_id": device_id},
                sort=[("stored_at", -1)]
            )
            
            if latest:
                devices.append({
                    "device_id": device_id,
                    "device_type": latest.get("device_type"),
                    "sensor_type": latest.get("sensor_type"),
                    "last_value": latest.get("value"),
                    "unit": latest.get("unit"),
                    "last_seen": latest.get("stored_at").isoformat() if isinstance(latest.get("stored_at"), datetime) else None
                })
        
        return {
            "status": "success",
            "count": len(devices),
            "devices": devices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查詢失敗: {str(e)}")

# ============ 啟動服務 ============
if __name__ == "__main__":
    print("=" * 60)
    print("IoT 資料查詢 API 服務")
    print("=" * 60)
    print()
    print("API 文件: http://localhost:8000/docs")
    print("API 根端點: http://localhost:8000/")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
