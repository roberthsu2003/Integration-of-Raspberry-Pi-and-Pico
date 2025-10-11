"""
專題模板 - Pi 主程式
功能：訂閱 MQTT 訊息、儲存到資料庫、提供 API 查詢
"""

import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mqtt_subscriber import MQTTSubscriber
from database import DatabaseManager
from models import SensorData, DeviceInfo
import config

# 初始化 FastAPI
app = FastAPI(title="學生專題 API")

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化資料庫
db = DatabaseManager(config.MONGODB_URI, config.DATABASE_NAME)

# 初始化 MQTT 訂閱者
mqtt_subscriber = None

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時執行"""
    global mqtt_subscriber
    
    print("=" * 50)
    print("啟動學生專題服務")
    print("=" * 50)
    
    # 連接資料庫
    db.connect()
    print(f"✓ 資料庫已連接: {config.DATABASE_NAME}")
    
    # 啟動 MQTT 訂閱者
    mqtt_subscriber = MQTTSubscriber(
        broker=config.MQTT_BROKER,
        port=config.MQTT_PORT,
        topics=config.MQTT_TOPICS,
        on_message_callback=handle_mqtt_message
    )
    mqtt_subscriber.start()
    print(f"✓ MQTT 訂閱已啟動: {config.MQTT_TOPICS}")
    
    print("=" * 50)
    print(f"API 服務運行於: http://0.0.0.0:{config.API_PORT}")
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉時執行"""
    if mqtt_subscriber:
        mqtt_subscriber.stop()
    db.disconnect()
    print("服務已關閉")

def handle_mqtt_message(topic, payload):
    """
    處理接收到的 MQTT 訊息
    
    Args:
        topic: MQTT 主題
        payload: 訊息內容（dict）
    """
    try:
        print(f"收到訊息 - 主題: {topic}")
        print(f"內容: {payload}")
        
        # 儲存到資料庫
        result = db.insert_sensor_data(payload)
        print(f"✓ 資料已儲存，ID: {result}")
        
    except Exception as e:
        print(f"處理訊息時發生錯誤: {e}")

# API 端點

@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "學生專題 API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "data": "/api/data",
            "devices": "/api/devices"
        }
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "database": "connected" if db.client else "disconnected",
        "mqtt": "connected" if mqtt_subscriber and mqtt_subscriber.is_connected else "disconnected"
    }

@app.get("/api/data")
async def get_all_data(limit: int = 100):
    """
    取得所有感測器資料
    
    Args:
        limit: 回傳資料筆數限制
    """
    try:
        data = db.get_all_data(limit=limit)
        return {
            "status": "success",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/{device_id}")
async def get_device_data(device_id: str, limit: int = 50):
    """
    取得特定裝置的資料
    
    Args:
        device_id: 裝置 ID
        limit: 回傳資料筆數限制
    """
    try:
        data = db.get_device_data(device_id, limit=limit)
        if not data:
            raise HTTPException(status_code=404, detail=f"找不到裝置 {device_id} 的資料")
        
        return {
            "status": "success",
            "device_id": device_id,
            "count": len(data),
            "data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/devices")
async def get_devices():
    """取得所有裝置列表"""
    try:
        devices = db.get_device_list()
        return {
            "status": "success",
            "count": len(devices),
            "devices": devices
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/data")
async def clear_all_data():
    """清除所有資料（謹慎使用）"""
    try:
        result = db.clear_all_data()
        return {
            "status": "success",
            "message": f"已刪除 {result} 筆資料"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.API_PORT,
        reload=True
    )
