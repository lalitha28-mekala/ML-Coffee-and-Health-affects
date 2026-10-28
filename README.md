# ☕ Coffee Intake & Health Condition Prediction

## 🔗 Live Demo
**Try the application:** [Coffee Health Prediction App](https://huggingface.co/spaces/Lalithamekala/ML_coffee_Health_affect)

## 📌 Project Overview

The Coffee Intake & Health Condition Prediction project explores the relationship between coffee consumption, lifestyle habits, and health-status categories using data analysis and machine learning.

The project provides an interactive application where users can explore data patterns and obtain a model-based prediction based on the available input features.

## 🎯 Objectives

- Explore coffee consumption and lifestyle-related data.
- Perform Exploratory Data Analysis (EDA) to identify patterns and trends.
- Prepare data for machine learning.
- Develop and evaluate a classification model.
- Present the project through an interactive Streamlit application.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Class Imbalance Handling:** Imbalanced-learn / SMOTE, if used in the final training pipeline
- **Web Application:** Streamlit

## 📊 Project Workflow

1. **Data Collection and Inspection** — Load the dataset and examine its structure, columns, and data types.
2. **Data Cleaning and Preprocessing** — Prepare the data for analysis and model training.
3. **Exploratory Data Analysis** — Explore distributions, class frequencies, and relationships between selected features.
4. **Model Development** — Train a classification model using the prepared data.
5. **Model Evaluation** — Evaluate performance using suitable classification metrics.
6. **Application Development** — Use Streamlit to present the project and model predictions interactively.

## 💡 Key Features

- Interactive application interface.
- Dataset exploration and visualizations.
- Coffee intake and lifestyle feature analysis.
- Machine-learning-based health-status classification.
- Prediction interface for entering feature values.

## 📁 Repository Structure

```text
Coffee-Health-Risk-Prediction/
│
├── app.py
├── pages/
│   ├── About.py
│   ├── EDA.py
│   ├── Model.py
│   └── Prediction.py
├── data/
│   └── clean_coffee_dataset.csv
├── models/
│   └── coffee_health_best_pipeline.pkl
├── assets/
│   └── style.css
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

*Update the filenames above to match the actual files committed to the repository.*

## 🚀 Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Coffee-Health-Risk-Prediction.git
cd Coffee-Health-Risk-Prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## 📷 Application Screenshots

Add screenshots of the actual running application here.

Suggested screenshots:

- Home page
- Exploratory Data Analysis page
- Model evaluation results
- Prediction page with sample output

## 📈 Learning Outcomes

- Practiced data inspection, cleaning, and preprocessing.
- Explored data distributions and relationships using visualizations.
- Gained practical experience with machine-learning classification workflows.
- Worked with a saved model pipeline and an interactive Streamlit interface.
- Practiced organizing a machine-learning project for portfolio presentation.

## ⚠️ Disclaimer

This project is intended for educational and demonstration purposes only. The predictions are not medically validated and must not be used for diagnosis, treatment, or other medical decisions.

## 👩‍💻 Author

**Lalitha Mekala**

- [GitHub](https://github.com/lalitha28-mekala)
- [Live Application](https://huggingface.co/spaces/Lalithamekala/ML_coffee_Health_affect)

