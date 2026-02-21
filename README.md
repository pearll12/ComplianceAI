# ComplianceAI — Data Policy Compliance Agent

An AI-powered compliance monitoring platform that converts unstructured policy documents into executable rules and continuously scans enterprise data to detect and explain policy violations.

---

## 🚀 Overview

Organizations store compliance policies in unstructured documents such as PDFs, while operational data changes continuously.  
This disconnect leads to undetected violations, regulatory risk, and costly audits.

**ComplianceAI bridges this gap** by automatically extracting rules from policy documents and applying them to enterprise datasets to enable continuous, explainable compliance monitoring.

---

## ✨ Key Features

- 📄 Policy-to-Rule Automation from PDF documents  
- 🔍 Automated violation detection on enterprise data  
- 🧾 Explainable compliance decisions with evidence  
- ⏱️ Continuous monitoring & real-time dashboards  
- 🤖 Self-improving rule optimization  
- 📊 Compliance analytics & reporting  

---

## 🧠 How It Works

1. **Policy Upload**  
   Users upload compliance policy PDFs.

2. **Rule Extraction**  
   NLP/LLM converts policy text into structured rules.

3. **Rule Execution**  
   Rules are applied to enterprise transaction data.

4. **Violation Detection**  
   Non-compliant records are flagged with explanations.

5. **Monitoring & Reporting**  
   Violations appear in dashboards and reports.

---

## 🧩 System Architecture

Policy PDF → Rule Extraction → Rule Engine → Data Scan → Violations → Dashboard

---

## 🖥️ Tech Stack

**Backend**
- Python
- FastAPI
- Pandas
- Rule Engine Logic

**NLP & Document Processing**
- PyMuPDF
- NLP / LLM-based parsing

**Database**
- PostgreSQL

**Frontend**
- React
- Chart.js / Visualization

---

## 📊 Dataset

IBM Transactions for Anti-Money Laundering (AML) dataset  
Synthetic financial transaction dataset with labeled laundering activity.

---

## 📈 Evaluation

Since the AML dataset contains ground-truth labels, detection performance is measured using:

- Precision  
- Recall  
- F1 Score  

The system also supports automated threshold optimization to improve rule effectiveness.

---

