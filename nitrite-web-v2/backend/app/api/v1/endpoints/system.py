from fastapi import APIRouter
import psutil
import platform
from datetime import datetime

router = APIRouter()


@router.get("/info")
async def get_system_info():
    """
    Récupérer les informations système complètes
    """
    # CPU Info
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    # Memory Info
    memory = psutil.virtual_memory()

    # Disk Info
    disk = psutil.disk_usage('/')

    # System Info
    uname = platform.uname()

    return {
        "system": {
            "os": uname.system,
            "os_version": uname.version,
            "hostname": uname.node,
            "architecture": uname.machine,
            "processor": uname.processor,
        },
        "cpu": {
            "cores": cpu_count,
            "usage_percent": cpu_percent,
            "frequency_mhz": cpu_freq.current if cpu_freq else None,
        },
        "memory": {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent,
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health")
async def system_health():
    """
    Vérifier la santé du système
    """
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    issues = []

    if cpu > 90:
        issues.append("High CPU usage")
    if memory.percent > 90:
        issues.append("High memory usage")
    if disk.percent > 90:
        issues.append("Low disk space")

    return {
        "status": "healthy" if not issues else "warning",
        "issues": issues,
        "metrics": {
            "cpu_percent": cpu,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent,
        }
    }


@router.post("/diagnostic")
async def run_diagnostic():
    """
    Lancer un diagnostic système complet
    """
    # TODO: Implement DISM, SFC scans, etc.

    return {
        "status": "started",
        "message": "Diagnostic started (not implemented yet)",
        "checks": [
            "DISM scan",
            "SFC scan",
            "Disk check",
            "Network check",
        ]
    }
