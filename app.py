import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="Coffee Health Risk App",
    layout="wide"
)

# ---------- Main Page ----------
st.title("☕ Coffee Health Risk Prediction App")
st.write("""
Welcome to the Coffee Health Risk Prediction App!  

This app helps you understand how your coffee consumption and lifestyle habits may impact your health.  
Navigate through the sidebar to explore different sections:  

- **About**: Learn the purpose of the app and how it works.  
- **EDA (Exploratory Data Analysis)**: Visualize trends and patterns in coffee consumption and health data.  
- **Model**: See the machine learning model built to predict health risks based on user data.  
- **Prediction**: Input your details to get a personalized health risk prediction and recommendations.  

Start by exploring the sections and discover insights about coffee and your health!
""")

