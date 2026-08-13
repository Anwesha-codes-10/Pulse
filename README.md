# 🏥 Pulse — Urban Infrastructure Decision Intelligence System

Pulse is a physics-informed machine learning engineering platform designed to treat municipal infrastructure assets like living patients. By mapping telemetry data to distinct digital twin states, Pulse diagnoses real-time structural anomalies, forecasts long-term structural decay curves, and delivers transparent, optimized treatment recommendations for city decision-makers.

Built during the **ML Empowerment Build Challenge 2.0**, Pulse completely avoids generic scratchpad scripts in favor of a production-ready, test-driven application architecture.

---

## 🚀 Core Value Proposition & Features

- 🏥 **Active Digital Twins:** Translates tabular database streams into distinct, asset-bound live state vectors (Bridges, Roads, Pipelines, Transformers) rather than processing anonymous data rows.
- ❤️ **Automated Diagnostics (XGBoost Classifier):** Instantly scans multi-sensor streams to detect discrete structural trauma anomalies (such as flash floods or freeze spikes).
- 📈 **Horizon Projections (XGBoost Regressor):** Projects structural degradation risks outward over 7, 30, and 90-day time horizons to enable proactive preventative maintenance.
- 🔄 **What-If Scenario Simulation (Bayesian Logic Network):** Allows operational stress testing (e.g., overriding traffic volume loads or weather severity) to compute real-time failure probabilities.
- 🛠️ **Multi-Objective Optimizer:** Balances competing constraints—risk mitigation, municipal cost minimization, asset life extension, and public urgency weights—to choose the single best action (**Repair, Delay, or Replace**).
- 🛡️ **Explainable Transparency:** Every decision carries a hard headline system confidence percentage and a localized **SHAP-style Feature Attribution breakdown** detailing exactly which sensor drove the recommendation.

---

## 🛠️ System Architecture & Folder Layout

Pulse follows a clear, lean separation of concerns designed for maximum local velocity and maintainability:

```text
pulse/
├── data/                  # Stratified local data storage (raw, processed, external)
├── logs/                  # Isolated runtime system logs
├── models/                # Serialized machine learning model artifacts
├── src/
│   ├── config/            # Strict central constants, platform paths, and logger profiles
│   ├── data/              # Cross-platform secure file loader and quality validation tools
│   ├── digital_twin/      # Immutable asset registries and live state tracker machines
│   ├── diagnosis/         # XGBoost classification training and prediction channels
│   ├── forecasting/       # XGBoost time-series regression projection engines
│   ├── bayesian/          # Probabilistic conditional scenario analysis simulations
│   ├── optimizer/         # Multi-objective decision matrix trade-off calculators
│   ├── explainability/    # Local SHAP weight attribution and confidence estimators
│   └── dashboard/         # Streamlit web user interface dashboard layout 
└── tests/                 # Automated test coverage matrix files
```

---

## ⚙️ Quickstart Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com
   cd pulse
   ```

2. **Setup Virtual Environment & Install Dependencies:**
   ```bash
   python -m venv .venv
   # On Windows PowerShell:
   .venv\Scripts\Activate.ps1
   
   pip install -r requirements.txt
   ```

3. **Launch the Active UI Dashboard:**
   ```bash
   python -m streamlit run src/dashboard/app.py
   ```
   *The interface will automatically spring to life at `http://localhost:8501`*

---

## 🧪 Robust Testing Layer

Pulse enforces strict behavioral verification across the entire data stream layer. To run all automated unit tests concurrently and verify core stability, execute the test runner inside your terminal:

```bash
python -m pytest -v
```

### Verified Test Matrix Modules:
- `test_config.py`: Validates architecture folder bootstrapping and configuration data immutability constraints.
- `test_loader.py`: Ensures platform-safe cross-platform file routing and defends strictly against malicious path-traversal vulnerabilities.
- `test_validator.py`: Audits clean data checking gates, missing value tolerances, and strict execution error boundaries.
- `test_twin_state.py`: Confirms live telemetry vital updates mapping cleanly to dictionary formats.
- `test_diagnosis.py`: Asserts correct training, evaluation accuracy, and out-of-sample prediction streams.
- `test_forecasting.py`: Verifies continuous timeline degradation vector calculations.
- `test_bayesian.py`: Validates probabilistic environmental stress accumulations.
- `test_optimizer.py`: Confirms decision matrix logic correctly balances costs and severe asset failures.
- `test_explainability.py`: Ensures feature attributions sum mathematically up to 100%.

---

## 💎 Engineering Highlights & Design Choices

1. **Flat Data Pipeline Over Heavy Cloud Databases:** Rather than introducing slow container networks, Pulse operates directly in local volatile memory structures and files—keeping dashboard calculations blazing fast and zero-latency.
2. **Fail-Fast Boundary Validation Check:** Every data ingestion row goes through a strict border control scan. If it hits unexpected columns or formatting drift, the system catches it early, logs a clean verification line, and handles it cleanly.
3. **Immutability Protection:** Core asset configurations rely on native Python frozen dataclasses. This ensures structural parameters (like unique ID tokens or location strings) remain unalterable and secure across execution threads.
