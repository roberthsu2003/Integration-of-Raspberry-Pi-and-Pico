#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多感測器儀表板 API
提供彙總查詢、多裝置資料比較和統計分析功能
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
import uvicorn

# ============ 資料模型 ============
class DeviceInfo(BaseModel):
    device_id: str
    device_name: str
    status: str
    last_seen: Optional[datetime]
    total_readings: int

class SensorReading(BaseModel):
    device_id: str
    value: float
    unit: str
    timestamp: datetime

class DeviceComparison(BaseModel):
    device_id: str
    average_value: float
    min_value: float
    max_value: float
    reading_count: int

class DashboardSummary(BaseModel):
    total_devices: int
    online_devices: int
    offline_devices: int
    total_readings_24h: int
    latest_readings: List[SensorReading]

# ============ FastAPI 應用程式 ============
app = FastAPI(title="多裝置儀表板 API", version="1.0.0")

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 連接
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["iot_data"]
devices_collection = db["devices"]
readings_collection = db["sensor_readings"]
alerts_collection = db["device_alerts"]

# ============ API 端點 ============

@app.get("/")
async def root():
    """API 根端點"""
    return {
        "message": "多裝置儀表板 API",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/api/dashboard",
            "devices": "/api/devices",
            "comparison": "/api/comparison",
            "statistics": "/api/statistics",
            "alerts": "/api/alerts"
        }
    }

@app.get("/api/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary():
    """
    取得儀表板摘要資訊
    包含裝置總數、線上/離線狀態、24小時讀數統計
    """
    try:
        # 計算裝置數量
        total_devices = devices_collection.count_documents({})
        online_devices = devices_collection.count_documents({"status": "online"})
        offline_devices = total_devices - online_devices
        
        # 計算 24 小時內的讀數
        cutoff_time = datetime.now() - timedelta(hours=24)
        total_readings_24h = readings_collection.count_documents({
            "stored_at": {"$gte": cutoff_time}
        })
        
        # 取得每個裝置的最新讀數
        pipeline = [
            {"$sort": {"stored_at": -1}},
            {"$group": {
                "_id": "$device_id",
                "latest_reading": {"$first": "$$ROOT"}
            }},
            {"$limit": 10}
        ]
        
        latest_readings_data = list(readings_collection.aggregate(pipeline))
        latest_readings = []
        
        for item in latest_readings_data:
            reading = item['latest_reading']
            latest_readings.append(SensorReading(
                device_id=reading['device_id'],
                value=reading['value'],
                unit=reading['unit'],
                timestamp=reading['stored_at']
            ))
        
        return DashboardSummary(
            total_devices=total_devices,
            online_devices=online_devices,
            offline_devices=offline_devices,
            total_readings_24h=total_readings_24h,
            latest_readings=latest_readings
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得儀表板資料失敗: {str(e)}")

@app.get("/api/devices")
async def get_all_devices():
    """取得所有裝置列表及其狀態"""
    try:
        devices = []
        for device in devices_collection.find():
            # 計算該裝置的總讀數
            total_readings = readings_collection.count_documents({
                "device_id": device['device_id']
            })
            
            devices.append({
                "device_id": device['device_id'],
                "device_name": device.get('device_name', device['device_id']),
                "status": device.get('status', 'unknown'),
                "last_seen": device.get('last_seen'),
                "location": device.get('location', 'unknown'),
                "total_readings": total_readings
            })
        
        return {"devices": devices, "count": len(devices)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得裝置列表失敗: {str(e)}")

@app.get("/api/devices/{device_id}")
async def get_device_detail(device_id: str):
    """取得特定裝置的詳細資訊"""
    try:
        device = devices_collection.find_one({"device_id": device_id})
        if not device:
            raise HTTPException(status_code=404, detail="找不到裝置")
        
        # 取得最新讀數
        latest_reading = readings_collection.find_one(
            {"device_id": device_id},
            sort=[("stored_at", -1)]
        )
        
        # 計算統計資訊
        cutoff_time = datetime.now() - timedelta(hours=24)
        pipeline = [
            {"$match": {
                "device_id": device_id,
                "stored_at": {"$gte": cutoff_time}
            }},
            {"$group": {
                "_id": None,
                "avg_value": {"$avg": "$value"},
                "min_value": {"$min": "$value"},
                "max_value": {"$max": "$value"},
                "count": {"$sum": 1}
            }}
        ]
        
        stats = list(readings_collection.aggregate(pipeline))
        
        device['_id'] = str(device['_id'])
        device['latest_reading'] = latest_reading
        device['statistics_24h'] = stats[0] if stats else None
        
        return device
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得裝置資訊失敗: {str(e)}")

@app.get("/api/comparison")
async def compare_devices(
    device_ids: str = Query(..., description="裝置 ID 列表，用逗號分隔"),
    hours: int = Query(24, description="統計時間範圍（小時）")
):
    """
    比較多個裝置的資料
    
    Args:
        device_ids: 裝置 ID 列表，例如 "pico_001,pico_002,pico_003"
        hours: 統計時間範圍（小時）
    """
    try:
        device_list = [d.strip() for d in device_ids.split(',')]
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        comparisons = []
        
        for device_id in device_list:
            pipeline = [
                {"$match": {
                    "device_id": device_id,
                    "stored_at": {"$gte": cutoff_time}
                }},
                {"$group": {
                    "_id": "$device_id",
                    "avg_value": {"$avg": "$value"},
                    "min_value": {"$min": "$value"},
                    "max_value": {"$max": "$value"},
                    "count": {"$sum": 1}
                }}
            ]
            
            result = list(readings_collection.aggregate(pipeline))
            
            if result:
                comparisons.append(DeviceComparison(
                    device_id=device_id,
                    average_value=round(result[0]['avg_value'], 2),
                    min_value=result[0]['min_value'],
                    max_value=result[0]['max_value'],
                    reading_count=result[0]['count']
                ))
            else:
                comparisons.append(DeviceComparison(
                    device_id=device_id,
                    average_value=0,
                    min_value=0,
                    max_value=0,
                    reading_count=0
                ))
        
        return {
            "time_range_hours": hours,
            "devices": comparisons
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"比較裝置資料失敗: {str(e)}")

@app.get("/api/statistics")
async def get_statistics(
    device_id: Optional[str] = Query(None, description="裝置 ID（可選）"),
    hours: int = Query(24, description="統計時間範圍（小時）")
):
    """
    取得統計資訊
    如果指定 device_id，回傳該裝置的統計；否則回傳所有裝置的彙總統計
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        match_query = {"stored_at": {"$gte": cutoff_time}}
        if device_id:
            match_query["device_id"] = device_id
        
        # 計算統計資訊
        pipeline = [
            {"$match": match_query},
            {"$group": {
                "_id": "$device_id" if not device_id else None,
                "avg_value": {"$avg": "$value"},
                "min_value": {"$min": "$value"},
                "max_value": {"$max": "$value"},
                "count": {"$sum": 1}
            }}
        ]
        
        results = list(readings_collection.aggregate(pipeline))
        
        if device_id:
            # 單一裝置統計
            if results:
                return {
                    "device_id": device_id,
                    "time_range_hours": hours,
                    "average_value": round(results[0]['avg_value'], 2),
                    "min_value": results[0]['min_value'],
                    "max_value": results[0]['max_value'],
                    "reading_count": results[0]['count']
                }
            else:
                return {
                    "device_id": device_id,
                    "time_range_hours": hours,
                    "message": "無資料"
                }
        else:
            # 所有裝置彙總統計
            return {
                "time_range_hours": hours,
                "devices": [
                    {
                        "device_id": r['_id'],
                        "average_value": round(r['avg_value'], 2),
                        "min_value": r['min_value'],
                        "max_value": r['max_value'],
                        "reading_count": r['count']
                    }
                    for r in results
                ]
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得統計資訊失敗: {str(e)}")

@app.get("/api/timeseries")
async def get_timeseries_data(
    device_id: str = Query(..., description="裝置 ID"),
    hours: int = Query(24, description="時間範圍（小時）"),
    interval_minutes: int = Query(60, description="資料點間隔（分鐘）")
):
    """
    取得時間序列資料（用於繪製圖表）
    
    Args:
        device_id: 裝置 ID
        hours: 時間範圍（小時）
        interval_minutes: 資料點間隔（分鐘）
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # 使用聚合管道取得平均值
        pipeline = [
            {"$match": {
                "device_id": device_id,
                "stored_at": {"$gte": cutoff_time}
            }},
            {"$sort": {"stored_at": 1}},
            {"$group": {
                "_id": {
                    "$subtract": [
                        {"$toLong": "$stored_at"},
                        {"$mod": [
                            {"$toLong": "$stored_at"},
                            interval_minutes * 60 * 1000
                        ]}
                    ]
                },
                "avg_value": {"$avg": "$value"},
                "timestamp": {"$first": "$stored_at"}
            }},
            {"$sort": {"timestamp": 1}}
        ]
        
        results = list(readings_collection.aggregate(pipeline))
        
        return {
            "device_id": device_id,
            "time_range_hours": hours,
            "interval_minutes": interval_minutes,
            "data_points": [
                {
                    "timestamp": r['timestamp'],
                    "value": round(r['avg_value'], 2)
                }
                for r in results
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得時間序列資料失敗: {str(e)}")

@app.get("/api/alerts")
async def get_alerts(
    device_id: Optional[str] = Query(None, description="裝置 ID（可選）"),
    limit: int = Query(50, description="最多回傳筆數")
):
    """取得警報記錄"""
    try:
        query = {"device_id": device_id} if device_id else {}
        alerts = alerts_collection.find(query).sort("created_at", -1).limit(limit)
        
        result = []
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            result.append(alert)
        
        return {"alerts": result, "count": len(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取得警報記錄失敗: {str(e)}")

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    try:
        # 測試資料庫連接
        mongo_client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"服務不健康: {str(e)}")

# ============ 啟動伺服器 ============
if __name__ == "__main__":
    print("多感測器儀表板 API")
    print("=" * 60)
    print("API 文件: http://localhost:8001/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
