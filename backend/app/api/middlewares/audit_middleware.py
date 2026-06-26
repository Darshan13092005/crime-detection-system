import time
import asyncio
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # We can extract user from request if authentication middleware adds it to request.state.user
        # For this prototype, we'll log the basic request info.
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        client_ip = request.client.host if request.client else "unknown"
        
        log_entry = {
            "method": request.method,
            "path": request.url.path,
            "ip": client_ip,
            "status_code": response.status_code,
            "duration": process_time
        }
        asyncio.create_task(self._log_audit(log_entry))
        return response

    async def _log_audit(self, entry: dict):
        # In a real system, insert this into an audit_logs table via Supabase or ELK
        print(f"[AUDIT] {entry['method']} {entry['path']} - IP: {entry['ip']} - Status: {entry['status_code']} - Time: {entry['duration']:.4f}s")
        
        # In a real app, you would insert this directly into `audit_logs` table in Supabase.
        # Example:
        # if not request.url.path.startswith("/docs"):
        return response
