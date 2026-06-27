# Healthcare Analytics Agent

## AI-Powered Healthcare Insurance Decision Intelligence Platform

---

# Project Vision

Healthcare Analytics Agent is a production-style AI-powered Healthcare Insurance Decision Intelligence Platform designed to automate the complete insurance analytics lifecycle.

Rather than functioning as a collection of isolated machine learning notebooks, the platform simulates an enterprise-grade insurance analytics system capable of transforming raw insurance portfolio data into actionable business intelligence through automated data engineering, predictive analytics, explainable AI, Retrieval-Augmented Generation (RAG), and conversational AI.

The platform combines actuarial analytics, machine learning, explainable AI, vector search, and Large Language Models into a unified decision-support system for insurers, underwriters, pricing analysts, actuaries, and business executives.

---

# Project Objectives

The platform automates the complete insurance analytics workflow by providing:

* Automated dataset management
* Data validation
* Data quality assessment
* Data preprocessing
* Feature engineering
* Portfolio segmentation
* Portfolio analytics
* Underwriting risk assessment
* Premium pricing prediction
* Lapse prediction
* Explainable AI
* Executive reporting
* Interactive dashboards
* AI-powered portfolio intelligence
* Retrieval-Augmented Generation (RAG)
* Enterprise AI Copilot

---

# Target Users

* Insurance Companies
* Health Insurers
* Underwriters
* Pricing Analysts
* Actuaries
* Portfolio Managers
* Risk Analysts
* Claims Analysts
* Business Executives

---

# End-to-End Workflow

```text
Launch Application
        │
        ▼
Detect Existing Portfolio
        │
        ├───────────────┐
        │               │
        ▼               ▼
 Continue         Replace Dataset
        │               │
        │         Upload New Dataset
        │               │
        └──────────────►
                Data Validation
                        │
                        ▼
                Data Preprocessing
                        │
                        ▼
               Feature Engineering
                        │
                        ▼
        Machine Learning Pipelines
        ┌─────────┬─────────┬─────────┐
        ▼         ▼         ▼
 Underwriting Pricing   Lapse
        └─────────┼─────────┘
                  ▼
         Portfolio Analytics
                  ▼
        Executive Reports
                  ▼
        Knowledge Base
                  ▼
      Embedding Generation
                  ▼
          Vector Database
                  ▼
             AI Copilot
                  ▼
     Interactive Dashboard
```

---

# Smart Dataset Management

The application maintains a persistent insurance portfolio rather than acting as a one-time analytics demo.

When launched:

* Existing portfolios are automatically loaded.
* Users can immediately access dashboards and reports.
* Users may replace the active portfolio with a new CSV dataset.
* Before replacement, the system warns that analytics will be regenerated.
* Once confirmed, the complete analytics pipeline executes automatically.

This mirrors enterprise insurance analytics platforms where a production dataset is continuously maintained.

---

# Automated Analytics Pipeline

Whenever a new portfolio is uploaded, the platform executes the following stages automatically.

## Data Validation

* Schema validation
* Missing value detection
* Duplicate detection
* Invalid value detection
* Outlier detection
* Data quality scoring

---

## Data Cleaning

* Missing value treatment
* Duplicate removal
* Data type correction
* Standardization
* Normalization
* Validation

---

## Feature Engineering

Automatically creates actuarial features including:

* Premium per Exposure
* Claims per Exposure
* Claim Frequency
* Claim Severity
* Loss Ratio
* Age Bands
* Seniority Bands
* Portfolio Segments
* Segment Scores
* Risk Scores

---

# Machine Learning Modules

## Underwriting Engine

Predicts

* Risk Class
* Underwriting Decision
* Prediction Confidence
* Decision Drivers

---

## Pricing Engine

Predicts

* Expected Claim Cost
* Recommended Premium
* Pricing Confidence
* Pricing Leakage

---

## Lapse Prediction Engine

Predicts

* Lapse Probability
* Revenue at Risk
* Customer Risk Segment
* Retention Priority
* Recommended Retention Action

---

# Portfolio Analytics

The Portfolio Analytics layer combines outputs from every machine learning module into a unified enterprise portfolio view.

Generated analytics include:

* Executive KPIs
* Portfolio Health Score
* Portfolio Profitability
* Risk Analytics
* Claims Analytics
* Pricing Analytics
* Retention Analytics
* Trend Analysis
* Executive Summary

---

# Explainable AI

Transparency is a core design principle.

Every machine learning prediction includes:

* SHAP Feature Importance
* Local SHAP Explanations
* Business Interpretation
* Decision Drivers
* Confidence Scores

This enables technical and non-technical users to understand how predictions were generated.

---

# AI Intelligence Layer

The project separates Machine Learning from Artificial Intelligence.

Machine Learning generates predictions.

Artificial Intelligence interprets those predictions and transforms them into business knowledge.

---

# Retrieval-Augmented Generation (RAG)

Instead of sending every report directly to the language model, the AI Copilot retrieves only the most relevant information from an indexed enterprise knowledge base.

The knowledge base is automatically created from project-generated artifacts.

Knowledge Sources

* Executive Reports
* Portfolio Analytics
* Pricing Reports
* Underwriting Reports
* Lapse Reports
* Validation Reports
* SHAP Explanations
* Portfolio Metrics
* Executive Summaries
* Markdown Reports
* JSON Reports

RAG Workflow

```text
Generated Reports
        │
        ▼
Document Chunking
        │
        ▼
Embedding Generation
        │
        ▼
Vector Database
        │
        ▼
Similarity Search
        │
        ▼
Relevant Context
        │
        ▼
Prompt Builder
        │
        ▼
Large Language Model
        │
        ▼
Grounded Response
```

Benefits

* Reduced hallucinations
* Grounded responses
* Faster retrieval
* Enterprise-scale architecture
* Explainable conversational analytics

---

# AI Copilot

The AI Copilot enables users to interact with the platform using natural language.

Example questions

* Why are claims increasing?
* Which customer segments are least profitable?
* Why was this premium recommended?
* Which applicants should be manually reviewed?
* Which customers are likely to lapse?
* Summarize the insurance portfolio.
* What business risks require immediate attention?
* Recommend actions to improve profitability.

The AI Copilot answers using:

* Portfolio Analytics
* Machine Learning Predictions
* SHAP Explanations
* Executive Reports
* Validation Reports
* Business Recommendations
* Retrieved Knowledge Base Context

Unlike a general-purpose chatbot, the AI Copilot grounds every response using Retrieval-Augmented Generation.

---

# Bring Your Own AI (BYO API)

The platform supports user-configurable AI providers.

Users can securely configure their preferred Large Language Model provider through the application settings.

Supported providers include:

* Google Gemini
* OpenAI
* Anthropic
* OpenRouter

Users can:

* Add their own API key
* Select AI provider
* Choose model
* Configure temperature
* Configure token limits
* Validate API connectivity

No API credentials are hardcoded within the project.

---

# Interactive Dashboard

The Streamlit dashboard serves as the primary business interface.

Modules include:

## Home

Displays

* Portfolio Overview
* Executive KPIs
* Dataset Information
* AI Executive Summary

---

## Portfolio Analytics

* Portfolio Health
* Risk Distribution
* Profitability
* Claims Analysis
* Trend Analysis

---

## Pricing Analytics

* Premium Prediction
* Pricing Calibration
* Residual Analysis
* Feature Importance

---

## Underwriting Analytics

* Risk Classification
* Decision Distribution
* SHAP Explanations
* Confusion Matrix

---

## Lapse Analytics

* Lapse Probability
* Revenue at Risk
* Retention Segments
* Customer Rankings

---

## AI Copilot

Natural language interface powered by Retrieval-Augmented Generation.

---

## Knowledge Base

Displays:

* Indexed Reports
* Document Count
* Embedding Status
* Vector Database Status
* Last Index Time

---

## Settings

Configure:

* AI Provider
* API Key
* Model Selection
* AI Parameters

---

## Reports

Export

* Executive Report
* Prediction Files
* Portfolio Reports
* Analytics Outputs

---

# Generated Outputs

## Data Outputs

* Processed Dataset
* Data Quality Report
* Feature Dictionary

---

## Underwriting Outputs

* Risk Classification
* Decision Recommendations
* SHAP Reports

---

## Pricing Outputs

* Premium Recommendations
* Expected Claims
* Feature Importance

---

## Lapse Outputs

* Lapse Predictions
* Retention Actions
* Revenue at Risk

---

## Portfolio Outputs

* Executive KPIs
* Portfolio Metrics
* Portfolio Health
* Trend Analytics
* Executive Summary

---

## AI Outputs

* Executive Reports
* Business Recommendations
* Conversational Responses
* Decision Explanations
* Knowledge Base
* AI Copilot Responses

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Data Processing

* Pandas
* NumPy

## Machine Learning

* Scikit-learn
* XGBoost

## Explainable AI

* SHAP

## Vector Database

* ChromaDB / FAISS

## Embeddings

* Sentence Transformers

## Large Language Models

* Google Gemini
* OpenAI
* Anthropic
* OpenRouter Compatible Models

---

# System Architecture

```text
                     Healthcare Analytics Agent

                               │
                               ▼
                      Dataset Management
                               │
                               ▼
                     Data Validation Layer
                               │
                               ▼
                     Data Preprocessing
                               │
                               ▼
                   Feature Engineering Layer
                               │
          ┌────────────────────┼────────────────────┐
          ▼                    ▼                    ▼
   Underwriting Engine   Pricing Engine    Lapse Engine
          └────────────────────┼────────────────────┘
                               ▼
                    Portfolio Analytics Layer
                               │
                               ▼
                  Explainability Layer (SHAP)
                               │
                               ▼
                  Executive Reports & Analytics
                               │
                               ▼
                    Embedding Generation
                               │
                               ▼
                        Vector Database
                               │
                               ▼
                      Similarity Retriever
                               │
                               ▼
                        Prompt Builder
                               │
                               ▼
                 User Selected Large Language Model
                               │
                               ▼
                         AI Copilot
                               │
                               ▼
                  Interactive Streamlit Dashboard
```

---

# Repository Structure

```text
Healthcare-Analytics-Agent/

├── data/
├── docs/
├── models/
├── outputs/
├── reports/
├── src/
│   ├── config/
│   ├── preprocessing/
│   ├── underwriting/
│   ├── pricing/
│   ├── lapse/
│   ├── portfolio/
│   ├── dashboard/
│   ├── copilot/
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── prompt_builder.py
│   │   └── llm.py
│   └── services/
└── README.md
```

---

# Key Features

* End-to-end automated insurance analytics pipeline
* Persistent portfolio management
* Automated feature engineering
* Multiple machine learning models
* Portfolio-wide business intelligence
* Explainable AI with SHAP
* Retrieval-Augmented Generation (RAG)
* Enterprise knowledge base
* Vector database integration
* AI Copilot with grounded responses
* User-configurable AI providers
* Bring Your Own API support
* Interactive Streamlit dashboard
* Modular production-ready architecture
* Automated executive reporting

---

# Future Roadmap

* Multi-user authentication
* Portfolio versioning
* Cloud deployment
* Database integration
* Scheduled analytics
* Model monitoring
* Agentic AI workflows
* Real-time portfolio updates
* Multi-portfolio comparison
* Enterprise role-based access control

---

# Final Deliverable

Healthcare Analytics Agent demonstrates how modern actuarial science, machine learning, explainable AI, Retrieval-Augmented Generation, vector databases, and Large Language Models can be integrated into a single production-ready Healthcare Insurance Decision Intelligence Platform.

Users can upload an insurance portfolio, automatically generate predictive analytics, explore interactive dashboards, export executive reports, and interact with a grounded AI Copilot that answers questions using the platform's own analytical outputs rather than relying solely on the underlying language model.

The project is designed to reflect enterprise software architecture and production-grade AI engineering practices while remaining modular, scalable, and extensible for future enhancements.
