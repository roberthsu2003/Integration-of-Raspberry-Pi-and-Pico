"""
資料模型定義
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class SensorData(BaseModel):
    """感測器資料模型"""
    device_id: str = Field(..., description="裝置 ID")
    timestamp: float = Field(..., description="時間戳記")
    data: Dict[str, Any] = Field(..., description="感測器資料")
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "pico_student_01",
                "timestamp": 1696000000.0,
                "data": {
                    "temperature": 25.5
                }
            }
        }

class DeviceInfo(BaseModel):
    """裝置資訊模型"""
    device_id: str
    device_name: Optional[str] = None
    last_seen: Optional[datetime] = None
    data_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "pico_student_01",
                "device_name": "學生專題裝置",
                "last_seen": "2025-10-11T10:30:00",
                "data_count": 150
            }
        }
