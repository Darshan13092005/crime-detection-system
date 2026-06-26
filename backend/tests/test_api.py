import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to Sentinel AI Backend"

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "cpu_usage" in data
    assert "database" in data

def test_login_mock():
    # Because of our mock login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@police.gov", "password": "any"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["access_token"] == "dummy-test-token"

def test_cameras_unauthorized():
    response = client.get("/api/v1/cameras/")
    # Should be unauthorized if no token
    assert response.status_code == 401

from unittest.mock import patch

def test_cameras_authorized():
    headers = {"Authorization": "Bearer dummy-test-token"}
    with patch("app.services.camera_service.CameraService.get_cameras") as mock_get_cameras:
        mock_get_cameras.return_value = [{
            "id": "cam-1", 
            "name": "Front Door", 
            "location": "Lobby", 
            "stream_url": "rtsp://...", 
            "is_active": True, 
            "created_at": "2026-06-24T00:00:00"
        }]
        response = client.get("/api/v1/cameras/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0

def test_analytics():
    headers = {"Authorization": "Bearer dummy-test-token"}
    with patch("app.api.routes.analytics.get_supabase_client"):
        response = client.get("/api/v1/analytics/", headers=headers)
        assert response.status_code == 200
        assert "total_incidents_today" in response.json()
