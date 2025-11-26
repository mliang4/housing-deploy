# MLE Side Project Roadmap & Tutorial

This document outlines a step-by-step guide to transforming your simple housing price API into a professional-grade Machine Learning Engineering (MLE) project.

## Phase 1: Experiment Tracking with MLflow

**Goal:** Stop guessing which hyperparameters worked best. Track every training run, including parameters, metrics, and the resulting model artifact.

### 1. Setup
Add `mlflow` to your `requirements.txt` and install it:
```bash
pip install mlflow
```

### 2. Modify `src/train.py`
Update your training script to log runs.

```python
import mlflow
import mlflow.sklearn
# ... existing imports ...

# Start an MLflow run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)
    
    # ... existing training code ...
    model.fit(X_train, y_train)
    
    # Log metrics
    score = model.score(X_test, y_test)
    mlflow.log_metric("r2_score", score)
    
    # Log the model itself
    mlflow.sklearn.log_model(model, "model")
    
    print(f"Model saved to MLflow with R2 score: {score}")
```

### 3. Run and View
Run your training script:
```bash
python src/train.py
```
Then view the dashboard:
```bash
mlflow ui
```
Open http://localhost:5000 to see your experiments.

---

## Phase 2: Data Versioning with DVC (Data Version Control)

**Goal:** Version control your large datasets just like you version control code, without bloating your git repository.

### 1. Setup
Install DVC:
```bash
pip install dvc
```

### 2. Initialize
Initialize DVC in your project root:
```bash
dvc init
```

### 3. Track Data
Assuming you have a data file (e.g., `data/housing.csv`). If you are fetching it dynamically in `train.py`, you should save it to disk first to version it.

```bash
# Download data manually or via script to data/housing.csv first
dvc add data/housing.csv
```
This creates `data/housing.csv.dvc`.

### 4. Git Tracking
Track the DVC pointer file with Git, but ignore the actual data:
```bash
git add data/housing.csv.dvc .gitignore
git commit -m "Start tracking data with DVC"
```

### 5. Remote Storage (Optional but recommended)
To simulate a cloud bucket locally:
```bash
mkdir c:\tmp\dvc-storage
dvc remote add -d myremote c:\tmp\dvc-storage
dvc push
```

---

## Phase 3: Model Monitoring with Evidently AI

**Goal:** Detect when your model's performance degrades because the real-world data has changed (Data Drift).

### 1. Setup
Add `evidently` to `requirements.txt`:
```bash
pip install evidently
```

### 2. Create a Monitoring Script
Create `src/monitor.py`. This script compares your "Reference" data (training data) with "Current" data (new incoming data).

```python
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def generate_drift_report(reference_data, current_data):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    report.save_html("drift_report.html")

# In a real app, 'current_data' would be logs from your API
```

### 3. Integrate
You can create a new API endpoint `/monitor` that triggers this report generation and returns the HTML or a JSON summary of drift status.

---

## Phase 4: Orchestration with Prefect

**Goal:** Automate the workflow. Instead of running scripts manually, define a robust pipeline that handles retries, scheduling, and logging.

### 1. Setup
Add `prefect` to `requirements.txt`:
```bash
pip install prefect
```

### 2. Create a Flow
Create `src/pipeline.py`.

```python
from prefect import task, flow
from src.train import train_model # You'll need to refactor train.py to export functions

@task
def get_data():
    # ... logic to fetch data ...
    return data

@task
def train(data):
    # ... logic to train ...
    return model

@flow(name="Housing Training Flow")
def main_flow():
    data = get_data()
    model = train(data)

if __name__ == "__main__":
    main_flow()
```

### 3. Run
```bash
python src/pipeline.py
```
Prefect provides a beautiful UI to see your flow runs.

---

## Phase 5: Feature Store with Feast

**Goal:** Solve the "training-serving skew" problem. Ensure the features you use for training are calculated exactly the same way when serving predictions.

### 1. Setup
```bash
pip install feast
```

### 2. Initialize
```bash
feast init feature_repo
cd feature_repo
```

### 3. Define Features
Edit `feature_repo/example.py` to define your data sources (e.g., Parquet files, SQL) and the features you want to extract (e.g., `MedInc`, `AveRooms`).

### 4. Apply
```bash
feast apply
```

### 5. Usage
In `train.py`:
```python
training_df = store.get_historical_features(...)
```

In `api.py`:
```python
features = store.get_online_features(...)
```

---

## Recommended Order of Execution

1.  **MLflow**: Easiest to add, high immediate value.
2.  **Prefect**: Helps organize your code as it grows.
3.  **DVC**: Essential once you start dealing with local CSV files or images.
4.  **Evidently**: Add this once you have the API running and want to simulate "production monitoring".
5.  **Feast**: This is the most complex. Save it for last as an advanced challenge.
