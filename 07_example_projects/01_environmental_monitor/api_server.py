"""
環境監測 API 服務
提供歷史資料查詢、統計分析和趨勢分析功能
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import pymongo
from config import *
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 建立 FastAPI 應用
app = FastAPI(
    title="環境監測 API",
    description="提供環境監測資料查詢和分析功能",
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

# MongoDB 連接
db_client = None
db = None
collection = None

@app.on_event("startup")
async def startup_db_client():
    """啟動時連接資料庫"""
    global db_client, db, collection
    try:
        db_client = pymongo.MongoClient(MONGO_URI)
        db = db_client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        logger.info(f"已連接到 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
    except Exception as e:
        logger.error(f"MongoDB 連接失敗: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """關閉時斷開資料庫連接"""
    global db_client
    if db_client:
        db_client.close()
        logger.info("已斷開 MongoDB 連接")

@app.get("/")
async def root():
    """根路徑"""
    return {
        "message": "環境監測 API 服務",
        "version": "1.0.0",
        "endpoints": {
            "latest": "/api/latest",
            "history": "/api/history",
            "stats": "/api/stats",
            "trend": "/api/trend"
        }
    }

@app.get("/health")
async def health_check():
    """健康檢查"""
    try:
        # 測試資料庫連接
        db_client.server_info()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.get("/api/latest")
async def get_latest_data(
    device_id: Optional[str] = Query(DEFAULT_DEVICE_ID, description="裝置 ID")
):
    """
    取得最新的感測器資料
    
    Args:
        device_id: 裝置 ID（選填）
    """
    try:
        query = {"device_id": device_id} if device_id else {}
        data = collection.find_one(
            query,
            {"_id": 0},
            sort=[("timestamp", pymongo.DESCENDING)]
        )
        
        if not data:
            raise HTTPException(status_code=404, detail="找不到資料")
        
        return {"status": "success", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查詢失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
async def get_history_data(
    device_id: Optional[str] = Query(DEFAULT_DEVICE_ID, description="裝置 ID"),
    hours: Optional[int] = Query(24, description="查詢最近幾小時的資料"),
    start: Optional[str] = Query(None, description="開始時間 (ISO 格式)"),
    end: Optional[str] = Query(None, description="結束時間 (ISO 格式)"),
    limit: int = Query(1000, description="最多回傳筆數")
):
    """
    查詢歷史資料
    
    Args:
        device_id: 裝置 ID
        hours: 查詢最近幾小時（如果未指定 start/end）
        start: 開始時間
        end: 結束時間
        limit: 最多回傳筆數
    """
    try:
        query = {"device_id": device_id} if device_id else {}
        
        # 時間範圍查詢
        if start and end:
            query["timestamp"] = {
                "$gte": start,
                "$lte": end
            }
        elif hours:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            query["timestamp"] = {"$gte": cutoff_time.isoformat()}
        
        # 查詢資料
        data = list(collection.find(
            query,
            {"_id": 0}
        ).sort("timestamp", pymongo.DESCENDING).limit(limit))
        
        return {
            "status": "success",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        logger.error(f"查詢失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_statistics(
    device_id: Optional[str] = Query(DEFAULT_DEVICE_ID, description="裝置 ID"),
    hours: int = Query(24, description="統計最近幾小時的資料")
):
    """
    取得統計資訊
    
    Args:
        device_id: 裝置 ID
        hours: 統計最近幾小時
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = {
            "device_id": device_id,
            "sensor_type": "temperature",
            "timestamp": {"$gte": cutoff_time.isoformat()}
        }
        
        # 使用聚合管道計算統計
        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": None,
                "count": {"$sum": 1},
                "average": {"$avg": "$value"},
                "min": {"$min": "$value"},
                "max": {"$max": "$value"},
                "std_dev": {"$stdDevPop": "$value"}
            }}
        ]
        
        result = list(collection.aggregate(pipeline))
        
        if not result:
            raise HTTPException(status_code=404, detail="找不到資料")
        
        stats = result[0]
        stats.pop("_id")
        
        # 四捨五入到小數點後 2 位
        for key in ["average", "min", "max", "std_dev"]:
            if key in stats and stats[key] is not None:
                stats[key] = round(stats[key], 2)
        
        return {
            "status": "success",
            "period": f"{hours} hours",
            "device_id": device_id,
            "statistics": stats
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"統計計算失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trend")
async def get_trend_analysis(
    device_id: Optional[str] = Query(DEFAULT_DEVICE_ID, description="裝置 ID"),
    hours: int = Query(24, description="分析最近幾小時的資料")
):
    """
    分析溫度趨勢
    
    Args:
        device_id: 裝置 ID
        hours: 分析最近幾小時
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        query = {
            "device_id": device_id,
            "sensor_type": "temperature",
            "timestamp": {"$gte": cutoff_time.isoformat()}
        }
        
        # 取得資料並按時間排序
        data = list(collection.find(
            query,
            {"_id": 0, "value": 1, "timestamp": 1}
        ).sort("timestamp", pymongo.ASCENDING))
        
        if len(data) < 2:
            raise HTTPException(status_code=404, detail="資料不足以分析趨勢")
        
        # 簡單的線性趨勢分析
        values = [d["value"] for d in data]
        n = len(values)
        
        # 計算平均變化率
        total_change = values[-1] - values[0]
        avg_change_rate = total_change / n
        
        # 判斷趨勢
        if avg_change_rate > 0.1:
            trend = "上升"
        elif avg_change_rate < -0.1:
            trend = "下降"
        else:
            trend = "穩定"
        
        # 計算波動性（標準差）
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        volatility = variance ** 0.5
        
        return {
            "status": "success",
            "period": f"{hours} hours",
            "device_id": device_id,
            "trend": trend,
            "data_points": n,
            "start_value": round(values[0], 2),
            "end_value": round(values[-1], 2),
            "total_change": round(total_change, 2),
            "avg_change_rate": round(avg_change_rate, 4),
            "volatility": round(volatility, 2)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"趨勢分析失敗: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"啟動 API 服務於 {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
