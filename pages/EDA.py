import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Set page config
st.set_page_config(page_title="Coffee Health Risk EDA", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("synthetic_coffee_health_10000.csv")
    
    # Cleaning and preprocessing
    df['Gender'] = df['Gender'].astype('category')
    df['Sleep_Quality'] = df['Sleep_Quality'].astype('category')
    df['Stress_Level'] = df['Stress_Level'].astype('category')
    df['Health_Issues'] = df['Health_Issues'].astype('category')
    df['Occupation'] = df['Occupation'].astype('category')

    df.rename(columns={'Coffee_Intake':'Coffee_Intake_Cups',
                       'Health_Issues':'Health_Status'}, inplace=True)

    df['Health_Status'] = df['Health_Status'].cat.add_categories("Healthy")
    df['Health_Status'] = df['Health_Status'].fillna('Healthy')
    df['Health_Status'] = df['Health_Status'].map({
        'Healthy': 'Healthy',
        'None': 'Healthy',
        'Mild': 'Mild Risk',
        'Moderate': 'Mild Risk',
        'Severe': 'High Risk'
    })
    return df

df = load_data()

# ------------------------------
# Page Title
# ------------------------------
st.title("📊 Exploratory Data Analysis (EDA)")
st.markdown("---")

# ------------------------------
# Dataset Overview
# ------------------------------
st.header("1. Dataset Overview")
st.write("### First 5 Rows")
st.dataframe(df.head())

st.write("### Dataset Information")
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()

st.text(s) 

st.write("### Summary Statistics (Numerical)")
st.dataframe(df.describe().T)

st.write("### Summary Statistics (Categorical)")
st.dataframe(df.describe(include='category').T)

# ------------------------------
# Univariate Analysis
# ------------------------------
st.header("2. Univariate Analysis")

# Numerical
st.subheader("Numerical Columns")
num_cols = df.select_dtypes(include=['int64','float64']).columns
for col in num_cols:
    st.markdown(f"**Distribution of {col}**")
    fig, ax = plt.subplots(1,2, figsize=(10,4))
    sns.histplot(df[col], kde=True, bins=20, ax=ax[0], color="skyblue")
    ax[0].set_title(f"Histogram of {col}")
    sns.boxplot(y=df[col], ax=ax[1], color="lightgreen")
    ax[1].set_title(f"Boxplot of {col}")
    st.pyplot(fig)

# Categorical
st.subheader("Categorical Columns")
cat_cols = df.select_dtypes(include=['category']).columns
for col in cat_cols:
    st.markdown(f"**Distribution of {col}**")
    fig, ax = plt.subplots(figsize=(6,4))
    sns.countplot(data=df, x=col, palette="Set2")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ------------------------------
# Bivariate Analysis
# ------------------------------
st.header("3. Bivariate Analysis")

# Numerical vs Target
st.subheader("Numerical vs Health_Status")
fig, ax = plt.subplots(2,4, figsize=(16,8))
sns.boxplot(data=df, y='Coffee_Intake_Cups', x='Health_Status', ax=ax[0,0])
sns.boxplot(data=df, y='Age', x='Health_Status', ax=ax[0,1])
sns.boxplot(data=df, y='Caffeine_mg', x='Health_Status', ax=ax[0,2])
sns.boxplot(data=df, y='Sleep_Hours', x='Health_Status', ax=ax[0,3])
sns.boxplot(data=df, y='BMI', x='Health_Status', ax=ax[1,0])
sns.boxplot(data=df, y='Heart_Rate', x='Health_Status', ax=ax[1,1])
sns.boxplot(data=df, y='Physical_Activity_Hours', x='Health_Status', ax=ax[1,2])
ax[1,3].axis('off')
plt.tight_layout()
st.pyplot(fig)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
fig, ax = plt.subplots(figsize=(10,6))
corr = df[num_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Pairplot
st.subheader("Pair Plot")
st.write("Showing pairwise relationships between features colored by Health_Status")
fig = sns.pairplot(df[num_cols.to_list() + ['Health_Status']], hue='Health_Status', corner=True, diag_kind="kde", palette="husl")
st.pyplot(fig)
