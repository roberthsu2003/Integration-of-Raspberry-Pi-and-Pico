"""
FastAPI 主應用程式
提供 RESTful API 端點用於物聯網資料管理

功能：
- 健康檢查
- 感測器資料的 CRUD 操作
- 裝置管理
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List, Optional
import uvicorn

# 匯入自訂模組
from models import SensorData, SensorDataResponse, Device, DeviceResponse, HealthResponse
from database import DatabaseManager

# 建立 FastAPI 應用程式實例
app = FastAPI(
    title="IoT Data API",
    description="物聯網資料收集和管理 API",
    version="1.0.0"
)

# 設定 CORS（跨來源資源共用）
# 允許前端應用程式從不同網域存取 API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境應該限制特定網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化資料庫管理器
db = DatabaseManager()

# ============================================================================
# 健康檢查端點
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """
    根路徑 - API 資訊
    """
    return {
        "status": "ok",
        "message": "IoT Data API is running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    健康檢查端點
    檢查 API 和資料庫連接狀態
    """
    try:
        # 測試資料庫連接
        db_status = db.check_connection()
        
        return {
            "status": "healthy" if db_status else "unhealthy",
            "message": "All systems operational" if db_status else "Database connection failed",
            "database": "connected" if db_status else "disconnected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "database": "error",
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# 感測器資料端點
# ============================================================================

@app.post("/api/data", response_model=SensorDataResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_data(data: SensorData):
    """
    新增感測器資料
    
    參數:
        data: 感測器資料物件
    
    返回:
        包含插入 ID 的回應
    """
    try:
        # 將資料轉換為字典
        data_dict = data.dict()
        
        # 如果沒有提供時間戳記，使用當前時間
        if "timestamp" not in data_dict or data_dict["timestamp"] is None:
            data_dict["timestamp"] = datetime.now()
        
        # 插入資料到資料庫
        result_id = db.insert_sensor_data(data_dict)
        
        return {
            "status": "success",
            "message": "Sensor data created successfully",
            "data": {
                "id": result_id,
                **data_dict
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sensor data: {str(e)}"
        )

@app.get("/api/data", response_model=SensorDataResponse)
async def get_all_sensor_data(
    limit: int = 100,
    skip: int = 0,
    device_id: Optional[str] = None,
    sensor_type: Optional[str] = None
):
    """
    查詢感測器資料
    
    參數:
        limit: 返回資料筆數上限（預設 100）
        skip: 跳過的資料筆數（用於分頁）
        device_id: 篩選特定裝置（選用）
        sensor_type: 篩選特定感測器類型（選用）
    
    返回:
        感測器資料列表
    """
    try:
        # 建立查詢過濾條件
        filter_dict = {}
        if device_id:
            filter_dict["device_id"] = device_id
        if sensor_type:
            filter_dict["sensor_type"] = sensor_type
        
        # 查詢資料
        data = db.query_sensor_data(filter_dict, limit=limit, skip=skip)
        
        return {
            "status": "success",
            "message": f"Retrieved {len(data)} records",
            "data": data,
            "count": len(data)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sensor data: {str(e)}"
        )

@app.get("/api/data/{device_id}", response_model=SensorDataResponse)
async def get_device_data(
    device_id: str,
    limit: int = 100,
    skip: int = 0
):
    """
    查詢特定裝置的感測器資料
    
    參數:
        device_id: 裝置 ID
        limit: 返回資料筆數上限
        skip: 跳過的資料筆數
    
    返回:
        該裝置的感測器資料列表
    """
    try:
        data = db.get_device_data(device_id, limit=limit, skip=skip)
        
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for device: {device_id}"
            )
        
        return {
            "status": "success",
            "message": f"Retrieved {len(data)} records for device {device_id}",
            "data": data,
            "count": len(data)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve device data: {str(e)}"
        )

@app.delete("/api/data/{device_id}")
async def delete_device_data(device_id: str):
    """
    刪除特定裝置的所有資料
    
    參數:
        device_id: 裝置 ID
    
    返回:
        刪除結果
    """
    try:
        deleted_count = db.delete_device_data(device_id)
        
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for device: {device_id}"
            )
        
        return {
            "status": "success",
            "message": f"Deleted {deleted_count} records for device {device_id}",
            "deleted_count": deleted_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete device data: {str(e)}"
        )

# ============================================================================
# 裝置管理端點
# ============================================================================

@app.get("/api/devices", response_model=DeviceResponse)
async def get_all_devices():
    """
    查詢所有裝置
    
    返回:
        裝置列表
    """
    try:
        devices = db.get_all_devices()
        
        return {
            "status": "success",
            "message": f"Retrieved {len(devices)} devices",
            "data": devices,
            "count": len(devices)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve devices: {str(e)}"
        )

@app.get("/api/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str):
    """
    查詢特定裝置資訊
    
    參數:
        device_id: 裝置 ID
    
    返回:
        裝置資訊
    """
    try:
        device = db.get_device(device_id)
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Device not found: {device_id}"
            )
        
        return {
            "status": "success",
            "message": "Device retrieved successfully",
            "data": [device]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve device: {str(e)}"
        )

# ============================================================================
# 應用程式啟動和關閉事件
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """應用程式啟動時執行"""
    print("=" * 50)
    print("IoT Data API 啟動中...")
    print("=" * 50)
    
    # 測試資料庫連接
    if db.check_connection():
        print("✓ 資料庫連接成功")
    else:
        print("✗ 資料庫連接失敗")
    
    print("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """應用程式關閉時執行"""
    print("IoT Data API 正在關閉...")
    db.close()
    print("資料庫連接已關閉")

# ============================================================================
# 主程式入口
# ============================================================================

if __name__ == "__main__":
    # 啟動 FastAPI 應用程式
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發模式：程式碼變更時自動重新載入
        log_level="info"
    )
