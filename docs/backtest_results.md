# EV Fleet Charging Optimization Backtest

## Objective

Evaluate the charging optimization engine against a First-Come-First-Serve (FCFS) baseline.

The optimizer considers:

* Vehicle risk score
* Required SOC for upcoming trips
* Station queue time
* Travel time to station
* Charging feasibility before departure

The FCFS baseline dispatches vehicles sequentially without optimization.

---

## Simulation Configuration

* Vehicles: 100
* Trips: 500
* Charging Stations: 10
* Simulation Cycles: 200
* Cycle Duration: 15 simulated minutes

---

# Optimizer Results

| Metric              | Value    |
| ------------------- | -------- |
| Completed Trips     | 197      |
| Pending Trips       | 303      |
| Charging Sessions   | 63       |
| Average Queue Time  | 14.0 min |
| Average Utilization | 60.62%   |

---

# FCFS Results

| Metric              | Value    |
| ------------------- | -------- |
| Completed Trips     | 143      |
| Pending Trips       | 357      |
| Charging Sessions   | 167      |
| Average Queue Time  | 14.0 min |
| Average Utilization | 60.61%   |

---

# Improvement

## Trip Completion

197 vs 143

Improvement:

```text
((197 - 143) / 143) × 100
= 37.76%
```

## Charging Sessions

63 vs 167

Reduction:

```text
((167 - 63) / 167) × 100
= 62.28%
```

---

# Conclusion

The optimization engine completed **37.76% more trips** than the FCFS baseline while requiring **62.28% fewer charging sessions**.

These results indicate that risk-aware charging decisions and intelligent station selection improve fleet efficiency compared to naive dispatch strategies.

The optimizer prioritizes vehicles based on trip urgency, battery deficit, and charging feasibility, enabling higher fleet productivity with fewer charging operations.
