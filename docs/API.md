# API Reference

The Sentinel AI backend is built with FastAPI. Interactive Swagger UI documentation is available automatically by navigating to `/docs` on your running backend server (e.g., `http://localhost:8000/docs`).

Below is a high-level overview of the exposed REST endpoints. All endpoints fall under the `/api/v1` prefix.

## Authentication
- `POST /auth/login`: Authenticate a user via Supabase and return a JWT access token.
- `POST /auth/register`: Register a new admin/commander account.

## Cameras
- `GET /cameras/`: List all registered cameras.
- `POST /cameras/`: Add a new RTSP camera stream for the AI to monitor.
- `DELETE /cameras/{camera_id}`: Remove a camera.

## Alerts
- `GET /alerts/`: Fetch historical alerts (supports filtering by severity and status).
- `PUT /alerts/{alert_id}`: Update an alert (e.g., mark it as `resolved`).

## Criminal Database
- `GET /criminals/`: Retrieve the list of known suspects.
- `POST /criminals/`: Add a new suspect (triggers embedding generation via InsightFace if an image is provided).

## Health
- `GET /health`: Used by PaaS load balancers (Render/Railway) to verify the API is alive.

### Authentication
All routes except `/auth/*` and `/health` require a valid JWT token passed in the header:
`Authorization: Bearer <token>`
