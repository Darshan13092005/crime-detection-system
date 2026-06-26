# User Manual for Sentinel AI

## Overview
Sentinel AI is designed for control room operators to monitor multiple camera feeds simultaneously while the AI automatically highlights critical events.

## 1. Logging In
Navigate to the web dashboard (e.g., `http://localhost:5173`).
Enter your credentials. Roles include:
- **Viewer**: Read-only access to cameras.
- **Operator**: Can acknowledge alerts.
- **Commander**: Can add new cameras and criminals.
- **Admin**: Full system access.

## 2. Dashboard Interface
- **Top Metrics**: Provides an immediate overview of active cameras and unacknowledged alerts.
- **Incident Chart**: Shows a 24-hour frequency plot of detected anomalies.
- **Recent Alerts**: A quick feed of the most critical recent events.

## 3. Camera Monitoring
Navigate to the **Live Monitoring** tab.
- Click on any camera feed to expand it.
- Bounding boxes will automatically appear in red if a weapon or violence is detected.
- Green bounding boxes indicate authorized personnel or recognized benign entities.

## 4. Managing Alerts
When an alert is generated:
1. Navigate to the **Alerts** tab.
2. Click on a specific alert to view the snapshot of the event.
3. Review the AI's confidence score.
4. Click **Acknowledge** or **Resolve** once security personnel have been dispatched or the threat is neutralized.

## 5. Adding Suspects
To add a known criminal to the facial recognition database:
1. Navigate to the **Criminal Database** tab.
2. Click **Add Profile**.
3. Upload a clear, front-facing image. The AI will automatically generate a facial encoding and store it securely.

## 6. Generating Reports
1. Go to the **Reports** tab.
2. Select a date range.
3. Click **Export PDF** for a formal handover document, or **Export CSV** for raw data analysis.
