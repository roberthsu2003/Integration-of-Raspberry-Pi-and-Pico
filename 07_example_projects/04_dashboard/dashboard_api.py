"""
儀表板 API 服務
提供資料查詢和圖表資料端點
"""

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import pymongo

# MongoDB 設定
MONGO_URI = "mongodb://admin:password123@localhost:27017/"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "sensor_logs"

app = FastAPI(title="儀表板 API")

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB 連接
db_client = None
collection = None

@app.on_event("startup")
async def startup():
    global db_client, collection
    db_client = pymongo.MongoClient(MONGO_URI)
    collection = db_client[MONGO_DB][MONGO_COLLECTION]

@app.on_event("shutdown")
async def shutdown():
    if db_client:
        db_client.close()

@app.get("/")
async def root():
    """提供儀表板 HTML"""
    return FileResponse("dashboard.html")

@app.get("/api/latest")
async def get_latest(device_id: str = Query("pico_001")):
    """取得最新資料"""
    data = collection.find_one(
        {"device_id": device_id},
        {"_id": 0},
        sort=[("timestamp", -1)]
    )
    return {"status": "success", "data": data}

@app.get("/api/history")
async def get_history(device_id: str = Query("pico_001"), hours: int = Query(24)):
    """取得歷史資料"""
    cutoff = datetime.now() - timedelta(hours=hours)
    data = list(collection.find(
        {"device_id": device_id, "timestamp": {"$gte": cutoff.isoformat()}},
        {"_id": 0}
    ).sort("timestamp", 1))
    return {"status": "success", "count": len(data), "data": data}

@app.get("/api/chart")
async def get_chart_data(device_id: str = Query("pico_001"), hours: int = Query(6)):
    """取得圖表資料"""
    cutoff = datetime.now() - timedelta(hours=hours)
    data = list(collection.find(
        {"device_id": device_id, "timestamp": {"$gte": cutoff.isoformat()}},
        {"_id": 0, "timestamp": 1, "value": 1}
    ).sort("timestamp", 1))
    
    labels = [d["timestamp"] for d in data]
    values = [d["value"] for d in data]
    
    return {
        "status": "success",
        "labels": labels,
        "values": values
    }

@app.get("/api/devices")
async def get_devices():
    """取得裝置列表"""
    devices = collection.distinct("device_id")
    return {"status": "success", "devices": devices}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
