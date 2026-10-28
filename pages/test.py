# pages/Prediction.py
import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="☕ Coffee & Health Predictor",
    page_icon="☕",
    layout="wide"
)

# -------------------------------
# Background & Styling
# -------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

div.block-container {
    background-color: rgba(255, 255, 255, 0.88);
    padding: 2rem 3rem;
    border-radius: 1rem;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
}

h1, h2, h3 {
    color: #4B3621;
}

.stButton>button {
    background-color: #6F4E37;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    padding: 10px 24px;
}

.stButton>button:hover {
    background-color: #4B3621;
    transform: scale(1.05);
}

/* Custom Title Styling */
.main-title {
    text-align: center;
    font-size: 42px;
    color: #6A1B9A; /* Deep purple */
    font-weight: bold;
    margin-bottom: 5px;
}
.sub-title {
    text-align: center;
    font-size: 20px;
    color: #2E7D32; /* Calm green */
    font-style: italic;
    margin-top: 0px;
    margin-bottom: 40px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# Load Model
# -------------------------------
with open("coffee_health_best_pipeline.pkl", "rb") as f:
    saved_data = pickle.load(f)

pipeline = saved_data.get("model")
mapping = saved_data.get("target_mapping")
reverse_mapping = saved_data.get("reverse_mapping")

if pipeline is None:
    st.error("❌ No valid model found in the pickle file. Please check the file contents.")

# -------------------------------
# Stylish Header Section
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 45px;
            font-weight: 800;
            color: #6C3483; /* Deep violet */
            font-family: 'Poppins', sans-serif;
            margin-bottom: 0px;
        }
        .subtitle {
            text-align: center;
            font-size: 22px;
            color: #4A235A; /* Muted plum */
            font-style: italic;
            font-family: 'Open Sans', sans-serif;
            margin-top: 5px;
        }
    </style>

    <h1 class="title">☕ COFFEE & HEALTH PREDICTOR</h1>
    <p class="subtitle">Unlock insights into your caffeine habits and wellness 🌱</p>
""", unsafe_allow_html=True)
# -------------------------------
# Coffee Caffeine Reference (mg per cup)
# -------------------------------
coffee_caffeine_dict = {
    "Decaf Coffee": 3,
    "Green Tea": 30,
    "Cold Coffee": 65,
    "Instant Coffee": 70,
    "Espresso": 65,
    "Cappuccino": 80,
    "Latte": 80,
    "Filter Coffee": 95,
    "Black Coffee": 110
}

# -------------------------------
# Helper Functions
# -------------------------------
def get_coffee_type(cups, caffeine_mg):
    if cups == 0 or caffeine_mg == 0:
        return "Zero Consumption", 0
    caffeine_per_cup = caffeine_mg / cups
    if 0 < caffeine_per_cup < 10:
        return "Decaf Coffee", 3
    elif 10 <= caffeine_per_cup < 45:
        return "Green Tea", 30
    elif 45 <= caffeine_per_cup < 60:
        return "Cold Coffee", 65
    elif 60 <= caffeine_per_cup < 75:
        return "Espresso", 65
    elif 75 <= caffeine_per_cup < 90:
        return "Latte/Cappuccino", 80
    elif 90 <= caffeine_per_cup < 100:
        return "Filter Coffee", 95
    elif 100 <= caffeine_per_cup < 120:
        return "Black Coffee", 110
    else:
        return "Other/Unknown", caffeine_per_cup

def calculate_caffeine(coffee_type, cups):
    return coffee_caffeine_dict.get(coffee_type, 0) * cups

def determine_sleep_quality(hours):
    if hours < 5:
        return "Poor"
    elif 5 <= hours < 7:
        return "Fair"
    elif 7 <= hours <= 9:
        return "Good"
    else:
        return "Excellent"

# -------------------------------
# User Inputs
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=4, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    country = st.text_input("Country", value="India")
    
    cups = st.number_input("☕ No. of Cups per Day", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
    coffee_type_input = st.selectbox(
        "Coffee Type (Optional, leave Auto-Detect)",
        ["Auto-Detect"] + list(coffee_caffeine_dict.keys())
    )
    
    if coffee_type_input == "Auto-Detect":
        caffeine_mg_input = st.number_input("Total Caffeine Intake (mg/day)", min_value=0.0, max_value=1000.0, value=95.0, step=1.0)
        coffee_type_detected, _ = get_coffee_type(cups, caffeine_mg_input)
        caffeine_mg = caffeine_mg_input
    else:
        coffee_type_detected = coffee_type_input
        caffeine_mg = calculate_caffeine(coffee_type_detected, cups)

    st.info(f"**Detected Coffee Type:** {coffee_type_detected}")
    st.info(f"**Estimated Daily Caffeine:** {caffeine_mg} mg")

    sleep_hours = st.number_input("😴 Sleep Hours (per night)", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
    sleep_quality = determine_sleep_quality(sleep_hours)
    st.info(f"**Sleep Quality:** {sleep_quality}")

    bmi = st.number_input("🏃‍♀️ BMI", min_value=10.0, max_value=50.0, value=22.0, step=0.1)

with col2:
    heart_rate = st.number_input("❤️ Resting Heart Rate (bpm)", min_value=30, max_value=200, value=70)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    physical_activity = st.number_input("Physical Activity (hours/week)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    occupation = st.text_input("Occupation", value="Other")
    smoking = st.selectbox("🚬 Smoking", ["No", "Yes"])
    alcohol = st.selectbox("🍷 Alcohol Consumption", ["No", "Yes"])

# Convert Yes/No to 0/1
smoking_val = 1 if smoking == "Yes" else 0
alcohol_val = 1 if alcohol == "Yes" else 0

# -------------------------------
# Prepare Input Data
# -------------------------------
user_input = pd.DataFrame({
    'Age': [age],
    'Gender': [gender],
    'Occupation': [occupation],
    'Coffee_Type': [coffee_type_detected],
    'Coffee_Intake_Cups': [cups],
    'Caffeine_mg': [caffeine_mg],
    'Sleep_Hours': [sleep_hours],
    'Sleep_Quality': [sleep_quality],
    'BMI': [bmi],
    'Heart_Rate': [heart_rate],
    'Stress_Level': [stress_level],
    'Physical_Activity_Hours': [physical_activity],
    'Smoking': [smoking_val],
    'Alcohol_Consumption': [alcohol_val]
})

# -------------------------------
# Prediction & Recommendations
# -------------------------------
if st.button("🔍 Predict Health Status"):
    if pipeline is not None:
        prediction_encoded = pipeline.predict(user_input)[0]
        prediction_label = reverse_mapping[prediction_encoded]
        st.success(f"### 🧠 Predicted Health Status: **{prediction_label}**")

        # -------------------------------
        # Gauge Chart for Caffeine Safety
        # -------------------------------
        if age <= 12:
            safe_caffeine = 45
        elif 13 <= age <= 17:
            safe_caffeine = 100
        elif 18 <= age <= 64:
            safe_caffeine = 400
        else:
            safe_caffeine = 250

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=caffeine_mg,
            delta={'reference': safe_caffeine, 'increasing': {'color': "red"}},
            gauge={
                'axis': {'range': [None, 600]},
                'bar': {'color': "#6F4E37"},
                'steps': [
                    {'range': [0, safe_caffeine*0.75], 'color': "lightgreen"},
                    {'range': [safe_caffeine*0.75, safe_caffeine], 'color': "skyblue"},
                    {'range': [safe_caffeine, 600], 'color': "tomato"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'value': safe_caffeine}
            },
            title={'text': f"Caffeine Intake vs Safe Limit ({safe_caffeine} mg/day)"}
        ))
        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # Recommendations Section
        # -------------------------------
        st.markdown("## 🌿 Personalized Recommendations")

        def card(content, color):
            st.markdown(
                f"""
                <div style='background-color:{color}; padding:12px; border-radius:10px; margin-bottom:10px'>
                {content}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Caffeine Suggestion
        if caffeine_mg > safe_caffeine:
            card(f"⚠️ Your caffeine intake (**{caffeine_mg} mg**) exceeds safe limit (**{safe_caffeine} mg**). Try switching to decaf or reducing cups.", "#ffcccc")
        else:
            card(f"✅ Your caffeine intake (**{caffeine_mg} mg**) is within healthy range!", "#d4edda")

        # BMI
        if bmi < 18.5:
            card("**BMI:** Underweight — Eat nutrient-rich foods and do resistance training.", "#f0e68c")
        elif 18.5 <= bmi <= 24.9:
            card("**BMI:** Normal — Maintain healthy diet and exercise.", "#d4edda")
        elif 25 <= bmi <= 29.9:
            card("**BMI:** Overweight — Increase activity, manage diet.", "#ffe5b4")
        else:
            card("**BMI:** Obese — Consult a doctor and follow structured diet plan.", "#ffcccc")

        # Sleep
        if sleep_hours < 6:
            card("**Sleep:** Less than recommended — Aim for 7–9 hrs of quality sleep.", "#ffcccc")
        elif 6 <= sleep_hours <= 9:
            card("**Sleep:** Optimal — Keep consistent sleep habits.", "#d4edda")
        else:
            card("**Sleep:** Excessive — Ensure balance with activity.", "#ffe5b4")

        # Stress
        if stress_level == "High":
            card("**Stress:** Practice meditation, yoga, or deep breathing regularly.", "#ffcccc")
        elif stress_level == "Medium":
            card("**Stress:** Manage through short breaks and mindful relaxation.", "#ffe5b4")
        else:
            card("**Stress:** Excellent balance! Maintain lifestyle.", "#d4edda")

        # Smoking & Alcohol
        if smoking == "Yes":
            card("**Smoking:** Strongly advised to quit — harms heart and lungs.", "#ffcccc")
        else:
            card("**Smoking:** Non-smoker — Great for long-term health.", "#d4edda")

        if alcohol == "Yes":
            card("**Alcohol:** Reduce frequency; opt for alcohol-free days weekly.", "#ffe5b4")
        else:
            card("**Alcohol:** Excellent — Staying alcohol-free supports liver and sleep.", "#d4edda")
