# Testing

The project uses pytest for validation of charging optimization logic.

Current Coverage:

* Total Coverage: 80%

Core Service Coverage:

* Risk Monitor Service: 100%
* Fleet Priority Service: 97%
* Station Service: 97%
* Charging Optimizer Service: 92%
* Queue Service: 89%
* Simulation Runner: 86%

Run Tests:

```bash
pytest -v
```

Generate Coverage Report:

```bash
pytest --cov=app
```
