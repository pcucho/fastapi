from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import platform
import psutil
import os

app = FastAPI(
    title="Wine Cellar API",
    description="API for Wine Cellar Authentication System",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Wine Cellar API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """
    Healthcheck endpoint
    Returns the health status of the application
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "wine-cellar-api"
        }
    )

@app.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed healthcheck endpoint
    Returns detailed system information and health metrics
    """
    try:
        # Get system information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "wine-cellar-api",
                "version": "1.0.0",
                "system": {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "hostname": platform.node(),
                    "processor": platform.processor(),
                    "python_version": platform.python_version()
                },
                "resources": {
                    "cpu": {
                        "usage_percent": cpu_percent,
                        "count": psutil.cpu_count()
                    },
                    "memory": {
                        "total_gb": round(memory.total / (1024 ** 3), 2),
                        "available_gb": round(memory.available / (1024 ** 3), 2),
                        "used_percent": memory.percent
                    },
                    "disk": {
                        "total_gb": round(disk.total / (1024 ** 3), 2),
                        "used_gb": round(disk.used / (1024 ** 3), 2),
                        "free_gb": round(disk.free / (1024 ** 3), 2),
                        "used_percent": disk.percent
                    }
                },
                "uptime": {
                    "process_id": os.getpid()
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "service": "wine-cellar-api",
                "error": str(e)
            }
        )

@app.get("/health/ready")
async def readiness_check():
    """
    Readiness check endpoint
    Checks if the service is ready to accept traffic
    """
    # Add your readiness checks here (database connections, external services, etc.)
    is_ready = True  # Replace with actual readiness logic
    
    if is_ready:
        return JSONResponse(
            status_code=200,
            content={
                "status": "ready",
                "timestamp": datetime.now().isoformat()
            }
        )
    else:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not ready",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/health/live")
async def liveness_check():
    """
    Liveness check endpoint
    Checks if the service is alive
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "alive",
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
