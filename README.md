# 🏥 Healthcare Insurance Decision Intelligence Platform

> An AI-powered end-to-end Healthcare Insurance Analytics Platform that streamlines underwriting, pricing, retention analysis, portfolio monitoring, business intelligence, and AI-assisted decision support.

<p align="center">

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)]()
[![XGBoost](https://img.shields.io/badge/XGBoost-Machine%20Learning-green.svg)]()
[![SHAP](https://img.shields.io/badge/SHAP-Explainable%20AI-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

</p>

---

## 📖 Overview

Healthcare insurers rely on multiple disconnected processes for underwriting, pricing, customer retention, portfolio monitoring, and reporting. This project consolidates these workflows into a single AI-powered decision intelligence platform.

The application enables users to upload healthcare insurance datasets, execute an automated analytics pipeline, visualize business insights through interactive dashboards, and interact with an AI Copilot for portfolio exploration.

The platform combines:

* 📊 Business Intelligence
* 🤖 Machine Learning
* 🔍 Explainable AI (SHAP)
* 📈 Interactive Analytics
* 💬 AI-assisted Decision Support

within a unified Streamlit application.

---

# ✨ Features

## 📤 Dataset Management

* Upload healthcare insurance datasets (CSV/XLSX)
* Automated dataset validation
* Data preprocessing
* Feature engineering
* Persistent portfolio management

---

## 🤖 Machine Learning Modules

### Underwriting Analytics

* Risk Classification
* Risk Score Prediction
* Underwriting Decision Support
* SHAP Explainability

### Pricing Analytics

* Claim Cost Prediction
* Premium Recommendation
* Premium Leakage Analysis

### Retention Analytics

* Lapse Prediction
* Customer Segmentation
* Revenue-at-Risk Analysis
* Retention Recommendations

---

## 📊 Business Intelligence

Interactive dashboards provide insights into:

* Executive KPIs
* Risk Distribution
* Claims Performance
* Pricing Performance
* Customer Retention
* Portfolio Trends

---

## 🤖 AI Copilot

The platform includes an AI-powered Copilot that helps users explore healthcare insurance portfolios using natural language.

Current capabilities include:

* Portfolio summarization
* Executive insight generation
* Analytics interpretation
* Business question answering
* Enterprise document upload
* Bring Your Own Gemini API Key (BYOK)

The Copilot uses the generated analytical outputs and uploaded enterprise documents as additional context whenever relevant.

---

# 🏗️ System Architecture

```text
                Upload Dataset
                      │
                      ▼
                Data Validation
                       │
                       ▼
               Data Preprocessing
                       │
                       ▼
              Feature Engineering
                       │
             ┌──────────┬──────────┬
             ▼          ▼          ▼
        Underwriting   Pricing   Retention
               └──────────┼──────────┘
                          ▼
                Portfolio Analytics
                          ▼
                Executive Dashboard
                          ▼
                    AI Copilot
                          ▼
                 Download Reports
```

---

# 🚀 Platform Workflow

```text
Upload Dataset
      │
      ▼
Validate Data
      │
      ▼
Preprocess Dataset
      │
      ▼
Run Analytics Pipeline
      │
      ▼
Generate Predictions
      │
      ▼
Business Intelligence Dashboards
      │
      ▼
AI Copilot
      │
      ▼
Download Reports
```

---

# 📊 Dashboard Modules

The platform consists of the following interactive pages:

* 🏠 Home
* 📤 Upload & Run
* 📊 Executive Dashboard
* ⚠️ Risk Analytics
* 🏥 Claims Analytics
* 💰 Pricing Analytics
* 🔄 Retention Analytics
* 📈 Trend Analytics
* 🤖 AI Copilot
* 📥 Download Center

---

# 🧠 Machine Learning Models

| Module            | Model              |
| ----------------- | ------------------ |
| Underwriting      | XGBoost Classifier |
| Pricing           | XGBoost Regressor  |
| Retention (Lapse) | XGBoost Classifier |

Model predictions are interpreted using **SHAP (SHapley Additive exPlanations)** to provide transparent and explainable insights.

---

# 💻 Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* XGBoost
* Scikit-learn

### Explainable AI

* SHAP

### Data Visualization

* Plotly

### Generative AI

* Google Gemini (Bring Your Own API Key)

### Utilities

* Joblib
* OpenPyXL

---

# 📂 Repository Structure

```text
Healthcare-Analytics-Agent/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── uploads/
│
├── docs/
│
├── models/
│   ├── underwriting/
│   ├── pricing/
│   └── lapse/
│
├── outputs/
│
├── reports/
│
├── src/
│   ├── dashboard/
│   ├── preprocessing/
│   ├── underwriting/
│   ├── pricing/
│   ├── lapse/
│   ├── portfolio/
│   ├── copilot/
│   ├── services/
│   ├── pipeline/
│   └── utils/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 📦 Installation

## Clone the repository

```bash
git clone https://github.com/veerkumarmodi76-afk/Healthcare-Analytics-Agent.git

cd Healthcare-Analytics-Agent
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
streamlit run app.py
```

---

# ▶️ Usage

1. Launch the Streamlit application.
2. Navigate to **Upload & Run**.
3. Upload a healthcare insurance dataset.
4. Execute the automated analytics pipeline.
5. Explore the generated dashboards.
6. Interact with the AI Copilot using your own Gemini API Key.
7. Download generated reports and analytics outputs.

---

# 📁 Dataset

This project uses the publicly available:

**Dataset of Health Insurance Portfolio**

* **Publisher:** Mendeley Data
* **access:** https://data.mendeley.com/datasets/386vmj2tbk/4 
* **Version:** 4 (2025)
* **DOI:** 10.17632/386vmj2tbk.4

### Dataset Characteristics

* 228,711 policy records
* 42 variables
* Healthcare insurance portfolio data (2017–2019)

### Citation

> Lledó, Josep; Espinosa Adamez, Priscila; Perez Gimenez, Virgilio (2025). Dataset of Health Insurance Portfolio. Mendeley Data. DOI: 10.17632/386vmj2tbk.4

---

# 🌐 Live Demo

**Streamlit Application**

https://healthcare-analytics-agent-4.streamlit.app/

---
# 👥 Team

## Project Lead
### Veer Kumar Modi

**Responsibilities**

- System Architecture
- Data Engineering
- Machine Learning Integration
- Dashboard Development
- AI Copilot
- Platform Integration

**GitHub:** https://github.com/veerkumarmodi76-afk

**LinkedIn:** https://www.linkedin.com/in/veerkumarmodi/

---
## Contributors

| Member                     | Responsibility              | LinkedIn                                                 |
| -------------------------- | --------------------------- | -------------------------------------------------------- |
| **Aishvarya Lukshme**      | Retention (Lapse) Analytics | https://www.linkedin.com/in/aishvarya-lukshme-16a126315/ |
| **Leandra Antony**         | Portfolio Analytics         | https://www.linkedin.com/in/leandra-antony-8359282b4/    |
| **Sivadharshini Thanapal** | Pricing Analytics           | https://www.linkedin.com/in/sivadharshini2710/           |
| **Bineetha V. S.**         | Data Validation             | https://www.linkedin.com/in/bineetha-v-s/                |
| **Sangamithra J. S.**      | Underwriting Analytics      | https://www.linkedin.com/in/sangamithra-j-s-ab7338375/   |

---

# 🚀 Future Improvements

Planned enhancements include:

* Retrieval-Augmented Generation (RAG)
* Enterprise Knowledge Base
* Vector Database Integration
* Multi-user Authentication
* Role-Based Access Control (RBAC)
* REST API
* Cloud-native Deployment
* Automated Model Monitoring
* Scheduled Model Retraining
* Portfolio Versioning
* Agentic AI Workflows

---

# 📜 License

This project is intended for educational and research purposes.

---

# 🙏 Acknowledgements

* Mendeley Data
* Streamlit
* XGBoost
* Scikit-learn
* SHAP
* Plotly
* Google Gemini

---

## ⭐ Support the Project

If you found this project useful or interesting, consider giving the repository a **⭐ Star** on GitHub.

It helps others discover the project and supports future development.
