# AI-Powered EV Fleet Charging Optimization Platform

## Overview

An intelligent EV fleet management platform that optimizes charging decisions for electric vehicle fleets.

The system analyzes:

* Vehicle battery levels
* Upcoming trips
* Charging station availability
* Queue times
* Fleet-wide charging demand

and automatically determines:

* Which vehicles should charge
* Which charging station should be selected
* Charging priority levels
* Fleet risk scores

---

## Features

### Fleet Optimization Engine

* Risk-based charging recommendations
* Priority queue generation
* Charging deficit calculation
* Station selection optimization

### Fleet Simulation Engine

* Vehicle trip simulation
* Battery consumption modeling
* Charging session simulation
* Time-based fleet operations

### Real-Time Updates

* WebSocket support
* Charging started events
* Charging completed events
* Vehicle available events
* Station utilization updates

### Redis Caching

Cached endpoints:

* GET /analytics/fleet
* GET /analytics/stations
* GET /fleet/priorities

### AI Operations Layer

#### Fleet Manager Agent

Answers:

* Which vehicles are critical?
* What needs attention right now?

#### Charging Advisor Agent

Answers:

* Why was vehicle selected?
* Which station should be used?

#### Analytics Agent

Answers:

* Fleet summary
* Station congestion analysis

#### What-If Agent

Answers:

* What if charging demand increases?
* What if chargers become unavailable?

---

## Tech Stack

Backend

* FastAPI
* Python

Database

* PostgreSQL
* SQLAlchemy
* Alembic

Caching

* Redis

Real-Time

* WebSockets

Infrastructure

* Docker

Testing

* Pytest

AI Layer

* Multi-Agent Architecture

---

## API Endpoints

### Fleet

GET /fleet/priorities

GET /fleet/charging

### Analytics

GET /analytics/fleet

GET /analytics/stations

### Simulation

POST /simulation/run-cycle

### AI

POST /ai/ask

### WebSocket

/ws/fleet

---

## Example AI Queries

Why was vehicle 117 selected?

Which vehicles are critical?

Summarize fleet health.

What should charge next?

What if 50 vehicles need charging at 6 PM?

---

## Running Locally

docker compose up -d

alembic upgrade head

python -m app.scripts.seed_data

uvicorn app.main:app --reload

---

## Test Coverage

pytest --cov=app

Current Coverage: 80%

---

## Author

Nitant Hedamba

