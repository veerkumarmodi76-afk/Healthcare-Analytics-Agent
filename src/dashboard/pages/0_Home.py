```python
"""
0_Home.py

Healthcare Insurance Decision Intelligence Platform

Enterprise Landing Page
------------------------------------
• Modern SaaS-inspired UI
• Platform Overview
• Quick Start Guide
• Workflow
• Execution Modes
• Professional Styling

Part 1
"""

from __future__ import annotations

import streamlit as st

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Healthcare Insurance Decision Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
    max-width:1400px;
}

h1,h2,h3{
    font-weight:700;
}

.hero{
    padding:45px;
    border-radius:20px;
    background:linear-gradient(135deg,#0F62FE,#42BE65);
    color:white;
    margin-bottom:25px;
}

.hero h1{
    font-size:42px;
    margin-bottom:10px;
}

.hero p{
    font-size:18px;
    line-height:1.7;
}

.metric-card{
    background:#fafafa;
    padding:20px;
    border-radius:15px;
    border:1px solid #e6e6e6;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
    height:150px;
}

.metric-card h2{
    color:#0F62FE;
    margin-bottom:10px;
}

.section-card{
    background:#ffffff;
    padding:28px;
    border-radius:18px;
    border:1px solid #ebebeb;
    margin-bottom:20px;
    box-shadow:0 2px 10px rgba(0,0,0,0.04);
}

.mode-card{
    background:#ffffff;
    padding:30px;
    border-radius:18px;
    border:2px solid #ececec;
    min-height:370px;
}

.mode-card h3{
    color:#0F62FE;
}

.step-card{
    background:#F8F9FA;
    border-left:5px solid #0F62FE;
    padding:18px;
    border-radius:10px;
    margin-bottom:15px;
}

.highlight{
    color:#0F62FE;
    font-weight:600;
}

.small{
    color:gray;
    font-size:14px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# HERO SECTION
# ==========================================================

st.markdown(
    """
<div class="hero">

# 🏥 Healthcare Insurance Decision Intelligence Platform

### AI-Powered Healthcare Insurance Analytics Platform

Transform healthcare insurance portfolios into actionable business intelligence using **Machine Learning**, **Explainable AI (SHAP)**, interactive dashboards, and an AI Copilot.

Designed for:

• Underwriters  
• Pricing Analysts  
• Portfolio Managers  
• Business Executives  
• Data Scientists

</div>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# QUICK LINKS
# ==========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.link_button(
        "🌐 Live Demo",
        "https://healthcare-analytics-agent-4.streamlit.app/",
        use_container_width=True,
    )

with col2:
    st.link_button(
        "💻 GitHub Repository",
        "https://github.com/veerkumarmodi76-afk/Healthcare-Analytics-Agent",
        use_container_width=True,
    )

with col3:
    st.link_button(
        "👤 Project Lead",
        "https://www.linkedin.com/in/veerkumarmodi",
        use_container_width=True,
    )

st.write("")

# ==========================================================
# PLATFORM SNAPSHOT
# ==========================================================

st.header("📊 Platform Snapshot")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
<div class="metric-card">

<h2>3</h2>

Machine Learning Models

Underwriting

Pricing

Retention

</div>
""",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
<div class="metric-card">

<h2>7+</h2>

Analytics Modules

Executive Dashboard

Claims

Pricing

Retention

</div>
""",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
<div class="metric-card">

<h2>AI</h2>

Enterprise Copilot

Portfolio Insights

Business Q&A

Document Context

</div>
""",
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        """
<div class="metric-card">

<h2>1 Click</h2>

Automated Pipeline

Validation

Preprocessing

Predictions

Dashboards

</div>
""",
        unsafe_allow_html=True,
    )

st.write("")

# ==========================================================
# ABOUT PLATFORM
# ==========================================================

st.header("📖 About the Platform")

st.markdown(
"""
The **Healthcare Insurance Decision Intelligence Platform** integrates multiple insurance analytics workflows into a single intelligent application.

Instead of relying on disconnected tools for underwriting, pricing, portfolio monitoring, and reporting, users can upload a healthcare insurance dataset and execute an automated analytics pipeline that produces interactive dashboards and business-ready insights.

The platform combines:

- 🤖 Machine Learning
- 📈 Business Intelligence
- 🔍 Explainable AI (SHAP)
- 💬 AI-Assisted Decision Support
- 📊 Interactive Dashboards

into one seamless experience.
"""
)

st.divider()

# ==========================================================
# PLATFORM WORKFLOW
# ==========================================================

st.header("🛣 Platform Workflow")

st.info(
"""
Every uploaded dataset follows the same standardized analytics pipeline.
"""
)

st.code(
"""
Upload Dataset
      │
      ▼
Automatic Validation
      │
      ▼
Data Preprocessing
      │
      ▼
Feature Engineering
      │
      ▼
Choose Execution Mode
      │
      ▼
Machine Learning Pipeline
      │
      ├────────► Underwriting
      │
      ├────────► Pricing
      │
      └────────► Retention
      │
      ▼
Portfolio Analytics
      │
      ▼
Executive Dashboard
      │
      ▼
AI Copilot
      │
      ▼
Download Reports
""",
language="text",
)

st.divider()

# ==========================================================
# GETTING STARTED
# ==========================================================

st.header("🚀 Getting Started")

step1, step2 = st.columns(2)

with step1:

    st.markdown(
        """
<div class="step-card">

### Step 1️⃣

Open **Upload & Run** from the navigation menu.

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="step-card">

### Step 2️⃣

Upload your Healthcare Insurance dataset.

Supported formats:

• CSV

• XLSX

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="step-card">

### Step 3️⃣

Choose the preferred execution mode.

Production Mode is recommended for most users.

</div>
""",
        unsafe_allow_html=True,
    )

with step2:

    st.markdown(
        """
<div class="step-card">

### Step 4️⃣

Run the complete analytics pipeline.

The platform automatically performs:

✔ Validation

✔ Preprocessing

✔ Predictions

✔ Portfolio Analytics

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="step-card">

### Step 5️⃣

Explore interactive dashboards.

Gain insights into:

• Risk

• Pricing

• Claims

• Retention

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="step-card">

### Step 6️⃣

Use the AI Copilot to explore your portfolio using natural language.

</div>
""",
        unsafe_allow_html=True,
    )

st.divider()

# ==========================================================
# EXECUTION MODES
# ==========================================================

st.header("⚙ Execution Modes")

prod, dev = st.columns(2)

with prod:

    st.markdown(
"""
<div class="mode-card">

# 🚀 Production Mode

### Recommended for Business Users

Uses pre-trained machine learning models for fast and reliable execution.

---

### Best For

✔ Portfolio Analysis

✔ Business Intelligence

✔ Executive Dashboards

✔ Daily Operations

✔ Production Deployment

---

### Advantages

• Fast Execution

• No Retraining Required

• Stable Predictions

• Lower Resource Usage

• Recommended for most users

</div>
""",
unsafe_allow_html=True,
)

with dev:

    st.markdown(
"""
<div class="mode-card">

# 🛠 Developer Mode

### Recommended for Data Scientists

Retrains machine learning models before generating predictions.

---

### Best For

✔ Research

✔ Feature Engineering

✔ Updated Datasets

✔ Model Development

✔ Experimentation

---

### Considerations

• Longer Execution Time

• Higher Compute Usage

• Model Retraining

• Intended for advanced users

</div>
""",
unsafe_allow_html=True,
)

st.success(
"""
💡 **Recommendation:** Unless you are developing or improving machine learning models, **Production Mode** is the preferred option. It reuses trained models to provide faster execution while maintaining consistent analytics results.
"""
)

st.divider()

# ==========================================================
# END OF PART 1
# ==========================================================
```
```python
# ==========================================================
# PLATFORM MODULES
# ==========================================================

st.header("📦 Platform Modules")

st.caption(
    "Each module focuses on a different stage of the healthcare insurance decision-making process."
)

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.subheader("📊 Executive Dashboard")

        st.write(
            """
The Executive Dashboard provides a high-level overview of portfolio performance through key business indicators.

**Highlights**

- Portfolio KPIs
- Premium Overview
- Claims Summary
- Risk Distribution
- Business Performance
"""
        )

    with st.container(border=True):

        st.subheader("⚠️ Underwriting Analytics")

        st.write(
            """
Predicts customer risk using machine learning.

**Capabilities**

- Risk Classification
- Underwriting Decision Support
- Risk Scores
- SHAP Explainability
- Individual Prediction Explanations
"""
        )

with col2:

    with st.container(border=True):

        st.subheader("💰 Pricing Analytics")

        st.write(
            """
Optimizes premium recommendations using predictive models.

**Capabilities**

- Claim Cost Prediction
- Premium Recommendation
- Pricing Performance
- Profitability Analysis
- Premium Leakage Analysis
"""
        )

    with st.container(border=True):

        st.subheader("🔄 Retention Analytics")

        st.write(
            """
Identifies customers likely to lapse and estimates business impact.

**Capabilities**

- Lapse Prediction
- Revenue at Risk
- Customer Segmentation
- Retention Recommendations
"""
        )

with col3:

    with st.container(border=True):

        st.subheader("📈 Portfolio Analytics")

        st.write(
            """
Provides comprehensive portfolio-level insights.

**Capabilities**

- Exposure Analysis
- Claims Analytics
- Portfolio Trends
- Executive Reports
- Business Intelligence
"""
        )

    with st.container(border=True):

        st.subheader("🤖 AI Copilot")

        st.write(
            """
Ask questions about your insurance portfolio using natural language.

**Capabilities**

- Portfolio Question Answering
- Executive Insight Generation
- Analytics Interpretation
- Explain Model Predictions
- Upload Enterprise Documents
- Bring Your Own Gemini API Key
"""
        )

st.divider()

# ==========================================================
# GENERATED OUTPUTS
# ==========================================================

st.header("📄 Generated Outputs")

left, right = st.columns(2)

with left:

    with st.container(border=True):

        st.subheader("🤖 Machine Learning Outputs")

        st.write(
            """
After executing the pipeline, the platform generates:

- Underwriting Predictions
- Premium Quotes
- Lapse Predictions
- SHAP Explanations
- Prediction Reports
- Model Metrics
"""
        )

with right:

    with st.container(border=True):

        st.subheader("📊 Business Intelligence Outputs")

        st.write(
            """
Business-ready reports include:

- Executive Dashboard
- Portfolio KPIs
- Pricing Reports
- Claims Analytics
- Trend Analysis
- Interactive Visualizations
"""
        )

st.divider()

# ==========================================================
# SUPPORTED INPUTS
# ==========================================================

st.header("📁 Supported Dataset Formats")

c1, c2 = st.columns([1, 2])

with c1:

    st.metric("Supported Formats", "CSV / XLSX")

with c2:

    st.info(
        """
Uploaded datasets are automatically validated before entering the analytics pipeline.

The platform performs preprocessing, feature engineering, and prediction generation with minimal user intervention.
"""
    )

st.divider()

# ==========================================================
# FAQ
# ==========================================================

st.header("❓ Frequently Asked Questions")

with st.expander("🚀 Which execution mode should I choose?"):

    st.write(
        """
For most users, **Production Mode** is recommended.

It loads the pretrained machine learning models and generates analytics significantly faster.

Choose **Developer Mode** only if you need to retrain or improve the models using new datasets.
"""
    )

with st.expander("🧠 Do I need to retrain the models every time?"):

    st.write(
        """
No.

Once trained, the platform stores the machine learning models and reuses them automatically in Production Mode.

Retraining is only necessary when introducing new data or improving the models.
"""
    )

with st.expander("📂 What datasets are supported?"):

    st.write(
        """
Supported formats include:

- CSV
- XLSX

The uploaded dataset should follow the healthcare insurance portfolio schema expected by the preprocessing pipeline.
"""
    )

with st.expander("🤖 What does the AI Copilot do?"):

    st.write(
        """
The AI Copilot can assist by:

- Explaining dashboard metrics
- Summarizing portfolio performance
- Interpreting machine learning outputs
- Answering business questions
- Using uploaded enterprise documents as additional context
"""
    )

st.divider()

# ==========================================================
# QUICK LINKS
# ==========================================================

st.header("🔗 Useful Links")

g1, g2, g3 = st.columns(3)

with g1:

    st.link_button(
        "💻 GitHub Repository",
        "https://github.com/veerkumarmodi76-afk/Healthcare-Analytics-Agent",
        use_container_width=True,
    )

with g2:

    st.link_button(
        "👤 Veer Kumar Modi",
        "https://www.linkedin.com/in/veerkumarmodi",
        use_container_width=True,
    )

with g3:

    st.link_button(
        "🌐 Live Demo",
        "https://healthcare-analytics-agent-4.streamlit.app/",
        use_container_width=True,
    )

st.divider()

# ==========================================================
# TEAM
# ==========================================================

st.header("👥 Development Team")

st.caption(
    "This platform was developed collaboratively as part of an AI-powered Healthcare Insurance Analytics project."
)

with st.container(border=True):

    st.subheader("🏆 Project Lead")

    st.markdown(
        """
### **Veer Kumar Modi**

**Responsibilities**

- Solution Architecture
- Data Engineering
- Machine Learning Integration
- Dashboard Development
- AI Copilot
- Platform Integration

🔗 **GitHub**

https://github.com/veerkumarmodi76-afk

🔗 **LinkedIn**

https://www.linkedin.com/in/veerkumarmodi
"""
    )

st.write("")

st.subheader("Contributors")

team = [
    (
        "Aishvarya Lukshme",
        "Retention (Lapse) Analytics",
        "https://www.linkedin.com/in/aishvarya-lukshme-16a126315/",
    ),
    (
        "Leandra Antony",
        "Portfolio Analytics",
        "https://www.linkedin.com/in/leandra-antony-8359282b4/",
    ),
    (
        "Sivadharshini Thanapal",
        "Pricing Analytics",
        "https://www.linkedin.com/in/sivadharshini2710/",
    ),
    (
        "Bineetha V. S.",
        "Data Validation",
        "https://www.linkedin.com/in/bineetha-v-s/",
    ),
    (
        "Sangamithra J. S.",
        "Underwriting Analytics",
        "https://www.linkedin.com/in/sangamithra-j-s-ab7338375/",
    ),
]

for name, role, linkedin in team:

    with st.container(border=True):

        c1, c2, c3 = st.columns([3, 3, 2])

        with c1:
            st.markdown(f"### {name}")

        with c2:
            st.write(role)

        with c3:
            st.link_button(
                "LinkedIn",
                linkedin,
                use_container_width=True,
            )

st.divider()

# ==========================================================
# PLATFORM SUMMARY
# ==========================================================

st.header("🎯 Platform Summary")

st.success(
    """
The **Healthcare Insurance Decision Intelligence Platform** unifies machine learning, business intelligence, explainable AI, and an AI-powered Copilot into a single decision support system.

Whether you are an underwriter, pricing analyst, portfolio manager, executive, or researcher, the platform enables you to transform raw healthcare insurance data into actionable insights through an automated end-to-end analytics workflow.
"""
)

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    """
---
<center>

### 🏥 Healthcare Insurance Decision Intelligence Platform

**Version 2.0**

Built with ❤️ using **Python**, **Streamlit**, **XGBoost**, **SHAP**, **Plotly**, and **Google Gemini**

**Project Repository**

https://github.com/veerkumarmodi76-afk/Healthcare-Analytics-Agent

**Project Lead**

Veer Kumar Modi

https://www.linkedin.com/in/veerkumarmodi

© 2026 Healthcare Insurance Decision Intelligence Platform

</center>
""",
    unsafe_allow_html=True,
)
```
