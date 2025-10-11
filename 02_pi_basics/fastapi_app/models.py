"""
資料模型定義
使用 Pydantic 進行資料驗證和序列化

Pydantic 提供：
- 自動資料驗證
- JSON 序列化/反序列化
- 型別提示
- API 文件自動生成
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Any
from datetime import datetime

# ============================================================================
# 感測器資料模型
# ============================================================================

class SensorData(BaseModel):
    """
    感測器資料模型
    
    用於接收和驗證來自 Pico 的感測器資料
    """
    device_id: str = Field(..., description="裝置唯一識別碼", example="pico_001")
    device_type: str = Field(default="pico_w", description="裝置類型", example="pico_w")
    timestamp: Optional[datetime] = Field(default=None, description="時間戳記")
    sensor_type: str = Field(..., description="感測器類型", example="temperature")
    value: float = Field(..., description="感測器數值", example=25.5)
    unit: str = Field(..., description="單位", example="celsius")
    location: Optional[str] = Field(default=None, description="位置", example="classroom_a")
    
    @validator('value')
    def validate_value(cls, v, values):
        """
        驗證感測器數值的合理範圍
        """
        sensor_type = values.get('sensor_type')
        
        # 溫度感測器的合理範圍
        if sensor_type == 'temperature':
            if v < -50 or v > 100:
                raise ValueError('Temperature value out of valid range (-50 to 100)')
        
        return v
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        """
        如果沒有提供時間戳記，使用當前時間
        """
        return v or datetime.now()
    
    class Config:
        # 允許使用 datetime 物件
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        # 範例資料（用於 API 文件）
        schema_extra = {
            "example": {
                "device_id": "pico_001",
                "device_type": "pico_w",
                "timestamp": "2025-01-11T10:30:00",
                "sensor_type": "temperature",
                "value": 25.5,
                "unit": "celsius",
                "location": "classroom_a"
            }
        }

class SensorDataResponse(BaseModel):
    """
    感測器資料回應模型
    
    用於 API 回應的標準格式
    """
    status: str = Field(..., description="狀態", example="success")
    message: str = Field(..., description="訊息", example="Data retrieved successfully")
    data: Optional[List[dict]] = Field(default=None, description="資料列表")
    count: Optional[int] = Field(default=None, description="資料筆數")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Data retrieved successfully",
                "data": [
                    {
                        "device_id": "pico_001",
                        "sensor_type": "temperature",
                        "value": 25.5,
                        "unit": "celsius",
                        "timestamp": "2025-01-11T10:30:00"
                    }
                ],
                "count": 1
            }
        }

# ============================================================================
# 裝置模型
# ============================================================================

class Device(BaseModel):
    """
    裝置資訊模型
    """
    device_id: str = Field(..., description="裝置唯一識別碼", example="pico_001")
    device_name: str = Field(..., description="裝置名稱", example="Temperature Sensor 1")
    device_type: str = Field(default="pico_w", description="裝置類型", example="pico_w")
    location: Optional[str] = Field(default=None, description="位置", example="classroom_a")
    status: str = Field(default="active", description="狀態", example="active")
    created_at: Optional[datetime] = Field(default=None, description="建立時間")
    last_seen: Optional[datetime] = Field(default=None, description="最後上線時間")
    
    @validator('status')
    def validate_status(cls, v):
        """驗證狀態值"""
        valid_statuses = ['active', 'inactive', 'maintenance', 'error']
        if v not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "device_id": "pico_001",
                "device_name": "Temperature Sensor 1",
                "device_type": "pico_w",
                "location": "classroom_a",
                "status": "active",
                "created_at": "2025-01-11T09:00:00",
                "last_seen": "2025-01-11T10:30:00"
            }
        }

class DeviceResponse(BaseModel):
    """
    裝置資訊回應模型
    """
    status: str = Field(..., description="狀態", example="success")
    message: str = Field(..., description="訊息", example="Devices retrieved successfully")
    data: Optional[List[dict]] = Field(default=None, description="裝置列表")
    count: Optional[int] = Field(default=None, description="裝置數量")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Devices retrieved successfully",
                "data": [
                    {
                        "device_id": "pico_001",
                        "device_name": "Temperature Sensor 1",
                        "device_type": "pico_w",
                        "location": "classroom_a",
                        "status": "active"
                    }
                ],
                "count": 1
            }
        }

# ============================================================================
# 健康檢查模型
# ============================================================================

class HealthResponse(BaseModel):
    """
    健康檢查回應模型
    """
    status: str = Field(..., description="狀態", example="healthy")
    message: str = Field(..., description="訊息", example="All systems operational")
    database: Optional[str] = Field(default=None, description="資料庫狀態", example="connected")
    version: Optional[str] = Field(default=None, description="API 版本", example="1.0.0")
    timestamp: str = Field(..., description="時間戳記")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "message": "All systems operational",
                "database": "connected",
                "version": "1.0.0",
                "timestamp": "2025-01-11T10:30:00"
            }
        }

# ============================================================================
# 錯誤回應模型
# ============================================================================

class ErrorResponse(BaseModel):
    """
    錯誤回應模型
    """
    status: str = Field(default="error", description="狀態")
    error_code: str = Field(..., description="錯誤代碼", example="DEVICE_NOT_FOUND")
    message: str = Field(..., description="錯誤訊息", example="Device not found")
    detail: Optional[str] = Field(default=None, description="詳細資訊")
    timestamp: str = Field(..., description="時間戳記")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "error_code": "DEVICE_NOT_FOUND",
                "message": "Device not found",
                "detail": "No device with ID 'pico_999' exists in the database",
                "timestamp": "2025-01-11T10:30:00"
            }
        }

# ============================================================================
# 查詢參數模型
# ============================================================================

class QueryParams(BaseModel):
    """
    查詢參數模型
    """
    limit: int = Field(default=100, ge=1, le=1000, description="返回資料筆數上限")
    skip: int = Field(default=0, ge=0, description="跳過的資料筆數")
    device_id: Optional[str] = Field(default=None, description="裝置 ID 篩選")
    sensor_type: Optional[str] = Field(default=None, description="感測器類型篩選")
    start_time: Optional[datetime] = Field(default=None, description="開始時間")
    end_time: Optional[datetime] = Field(default=None, description="結束時間")
    
    class Config:
        schema_extra = {
            "example": {
                "limit": 100,
                "skip": 0,
                "device_id": "pico_001",
                "sensor_type": "temperature",
                "start_time": "2025-01-11T00:00:00",
                "end_time": "2025-01-11T23:59:59"
            }
        }
