# 🚗 AI-Powered EV Fleet Charging Optimization Platform

## Live Demo

API Documentation:

https://ev-fleet-management-mekv.onrender.com/docs

---

# Overview

The AI-Powered EV Fleet Charging Optimization Platform is an intelligent fleet management system designed to optimize charging decisions for electric vehicle fleets.

Traditional fleet management systems often charge vehicles using simple rules such as:

* First Come First Serve (FCFS)
* Fixed battery thresholds
* Manual charging decisions

These approaches frequently lead to:

* Charger congestion
* Unnecessary charging sessions
* Vehicle downtime
* Missed trips
* Poor fleet utilization

This platform introduces a risk-based charging optimization engine that continuously evaluates:

* Vehicle battery levels
* Upcoming trip requirements
* Trip urgency
* Charging station availability
* Charger occupancy
* Queue delays

and automatically determines:

* Which vehicles should charge
* Which station should be selected
* Charging priority levels
* Charging targets
* Fleet risk status

The system also includes real-time updates, Redis caching, simulation-based backtesting, and an AI operations layer capable of answering fleet-related questions.

---

# Key Features

## Intelligent Charging Optimization

The optimization engine evaluates fleet-wide charging demand and prioritizes vehicles based on:

* Battery deficit
* Required State of Charge (SOC)
* Upcoming trip urgency
* Charging station availability
* Charging delay impact

The optimizer generates:

* Risk scores
* Priority levels
* Charging recommendations
* Station recommendations

---

## Fleet Simulation Engine

A complete simulation environment models:

* Vehicle dispatch
* Trip execution
* Battery consumption
* Charging sessions
* Vehicle returns

This allows realistic testing of charging strategies before deployment.

---

## Risk Monitoring System

Each vehicle is continuously analyzed to determine:

* Projected battery level
* Required battery level
* Charging deficit
* Risk score

Vehicles are automatically classified into:

* LOW
* MEDIUM
* HIGH
* CRITICAL

priority categories.

---

## Dynamic Charging Dispatch

Vehicles are automatically dispatched to charging stations when:

* Charging is required
* Chargers are available
* The recommendation is feasible

The system dynamically manages charger allocation and utilization.

---

## Real-Time WebSocket Events

The platform provides live fleet updates using WebSockets.

Examples:

### Charging Started

```json
{
  "event": "charging_started",
  "vehicle_id": 117,
  "station": "Gift City Supercharger",
  "target_soc": 80
}
```

### Charging Completed

```json
{
  "event": "charging_completed",
  "vehicle_id": 117,
  "soc": 80
}
```

### Vehicle Available

```json
{
  "event": "vehicle_available",
  "vehicle_id": 117
}
```

### Station Utilization Updated

```json
{
  "event": "station_utilization_updated",
  "station": "Gift City Supercharger"
}
```

---

## Redis Caching Layer

To reduce database load and improve API response times, Redis caching is used.

Cached Endpoints:

### Fleet Analytics

```http
GET /analytics/fleet
```

### Station Analytics

```http
GET /analytics/stations
```

### Fleet Priorities

```http
GET /fleet/priorities
```

Cache invalidation occurs automatically after simulation cycles.

---

## AI Operations Layer

The platform includes a multi-agent AI layer capable of answering operational questions.

### Fleet Manager Agent

Answers:

* Which vehicles are critical?
* What requires attention right now?
* What is the fleet health?

---

### Charging Advisor Agent

Answers:

* Why was vehicle selected?
* Why was a station selected?
* What should charge next?

---

### Analytics Agent

Answers:

* Fleet summary
* Station utilization
* Fleet statistics

---

### What-If Agent

Answers:

* What if charging demand doubles?
* What if chargers become unavailable?
* What if 50 vehicles need charging at 6 PM?

This enables simulation-driven operational planning.

---

# System Architecture

```text
                     +----------------------+
                     |      AI Agents       |
                     |----------------------|
                     | Fleet Manager        |
                     | Charging Advisor     |
                     | Analytics Agent      |
                     | What-If Agent        |
                     +----------+-----------+
                                |
                                v

+-------------+      +----------------------+
| WebSockets  |----->|     FastAPI API      |
+-------------+      +----------------------+
                                |
          +---------------------+---------------------+
          |                     |                     |
          v                     v                     v

+----------------+    +----------------+    +----------------+
| Redis Cache    |    | Optimizer      |    | Simulation     |
+----------------+    +----------------+    +----------------+
                                |
                                v

                     +----------------------+
                     | PostgreSQL Database  |
                     +----------------------+
```

---

# Technology Stack

## Backend

* Python
* FastAPI

## Database

* PostgreSQL
* SQLAlchemy
* Alembic

## Caching

* Redis

## Real-Time Communication

* WebSockets

## Infrastructure

* Docker
* Render

## Testing

* Pytest
* pytest-cov

## AI Layer

* Multi-Agent Architecture

---

# API Endpoints

## Fleet

```http
GET /fleet/priorities
GET /fleet/charging
```

---

## Analytics

```http
GET /analytics/fleet
GET /analytics/stations
```

---

## Simulation

```http
POST /simulation/run-cycle
GET /simulation/status
```

---

## AI

```http
POST /ai/ask
```

Example:

```text
Which vehicles are critical?

Summarize fleet health

Why was vehicle 119 selected?

Show station utilization
```

---

## WebSocket

```http
/ws/fleet
```

---

# Backtesting Results

The optimizer was compared against a First-Come-First-Serve charging strategy.

## Intelligent Optimizer

* Completed Trips: 197
* Pending Trips: 303
* Charging Sessions: 63
* Rejected Dispatches: 317
* Average Queue Time: 14 minutes
* Average Utilization: 60.62%

---

## FCFS Baseline

* Completed Trips: 143
* Pending Trips: 357
* Charging Sessions: 167
* Rejected Dispatches: 24
* Average Utilization: 60.61%

---

## Result

The optimizer achieved significantly more completed trips while reducing unnecessary charging activity through intelligent charger allocation.

---

# Test Coverage

Current coverage:

```text
80%+
```

Run:

```bash
pytest --cov=app
```

---

# Running Locally

## Clone Repository

```bash
git clone https://github.com/Nitant4806/ev-fleet-management.git
cd ev-fleet-management
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run PostgreSQL and Redis

```bash
docker compose up -d
```

---

## Apply Migrations

```bash
alembic upgrade head
```

---

## Seed Data

```bash
python -m app.scripts.seed_data
```

---

## Start Server

```bash
uvicorn app.main:app --reload
```

---

# Future Enhancements

* LangGraph-based autonomous agents
* Predictive charging demand forecasting
* Fleet-wide reinforcement learning optimization
* Real-time map visualization
* Celery-based background task processing
* Multi-fleet support
* Cost-aware charging optimization

---

# Author

Nitant Hedamba

Final-Year B.Tech Student

Backend Engineering • Distributed Systems • EV Fleet Optimization
