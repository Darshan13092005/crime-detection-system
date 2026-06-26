# Sentinel AI - Live Demo Script for Judges

**Estimated Time**: 5-7 Minutes

## 1. Introduction (1 min)
*Start on the Dashboard Overview screen.*
"Hello judges, we are presenting Sentinel AI. Currently, security guards stare at dozens of screens, inevitably missing critical events due to fatigue. Sentinel AI solves this. What you're looking at is our React-based control room dashboard, which gives a high-level view of our entire security network."

## 2. Live Monitoring & Threat Detection (2 mins)
*Navigate to the 'Live Monitoring' / 'Cameras' tab.*
"Here are our live camera feeds. Behind the scenes, our FastAPI backend is running a multi-threaded Python application. It uses YOLOv8 for weapon and violence detection, and InsightFace for facial recognition."
*(Hold up a toy weapon or show a pre-recorded test video feed containing a weapon).*
"As you can see, the moment a threat enters the frame, a red bounding box is drawn, and the system immediately registers this."

## 3. Alerts & Dispatch (1.5 mins)
*Navigate to the 'Alerts' tab.*
"If you look at the Alerts tab, the system instantly generated a 'Critical' alert. It saved a snapshot of the exact moment as evidence. At this exact time, our system also fired a Webhook to notify security personnel on their phones via Telegram so they can respond instantly."
*(Show how an operator clicks 'Acknowledge' to clear the alert).*

## 4. Criminal Database Management (1 min)
*Navigate to the 'Criminal Database' tab.*
"We also support proactive searching. If the police give us a photo of a wanted suspect, we upload it here. InsightFace creates a vector embedding of the face. If that suspect walks past any of our cameras, the system will flag a 'Criminal Spotted' alert."

## 5. Enterprise Features & Conclusion (1 min)
*Navigate to the 'Reports' tab and demonstrate Light/Dark mode toggle.*
"For enterprise compliance, we implemented Role-Based Access Control so only Admins can delete data. We also have a Reports generation tool that exports incident data to PDF and CSV for law enforcement handover. 
Thank you. We'd love to answer any questions."
