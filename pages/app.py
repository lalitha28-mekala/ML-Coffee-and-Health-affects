# pages/Prediction.py
import streamlit as st
import pandas as pd
import pickle

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Coffee & Health Predictor",
    page_icon="☕",
    layout="wide"
)

# -------------------------------
# Load Model
# -------------------------------
with open("coffee_health_best_pipeline.pkl", "rb") as f:
    saved_data = pickle.load(f)

pipeline = saved_data.get("model")
mapping = saved_data.get("target_mapping")
reverse_mapping = saved_data.get("reverse_mapping")

if pipeline is None:
    st.error("No valid model found in the pickle file. Check your pickle contents.")

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
# App Title
# -------------------------------
st.title("☕ Coffee & Health Predictor")
st.markdown("Enter your details below to predict your Health Status and get lifestyle recommendations:")

# -------------------------------
# User Inputs
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=4, max_value=100, value=30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    country = st.text_input("Country", value="India")
    
    cups = st.number_input("No. of Cups per Day", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
    coffee_type_input = st.selectbox(
        "Coffee Type (Optional, leave if unknown)",
        ["Auto-Detect"] + list(coffee_caffeine_dict.keys())
    )
    
    if coffee_type_input == "Auto-Detect":
        caffeine_mg_input = st.number_input("Total Caffeine Intake (mg/day)", min_value=0.0, max_value=1000.0, value=95.0, step=1.0)
        coffee_type_detected, _ = get_coffee_type(cups, caffeine_mg_input)
        caffeine_mg = caffeine_mg_input
    else:
        coffee_type_detected = coffee_type_input
        caffeine_mg = calculate_caffeine(coffee_type_detected, cups)

    st.info(f"Coffee Type: {coffee_type_detected}")
    st.info(f"Estimated daily caffeine: {caffeine_mg} mg")
    
    sleep_hours = st.number_input("Sleep Hours (per night)", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
    sleep_quality = determine_sleep_quality(sleep_hours)
    st.info(f"Calculated Sleep Quality: {sleep_quality}")
    
    bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0, step=0.1)

with col2:
    heart_rate = st.number_input("Resting Heart Rate (bpm)", min_value=30, max_value=200, value=70)
    stress_level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    physical_activity = st.number_input("Physical Activity (hours/week)", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
    occupation = st.text_input("Occupation", value="Other")
    smoking = st.selectbox("Smoking", ["No", "Yes"])
    alcohol = st.selectbox("Alcohol Consumption", ["No", "Yes"])

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
if st.button("Predict Health Status"):
    if pipeline is not None:
        prediction_encoded = pipeline.predict(user_input)[0]
        prediction_label = reverse_mapping[prediction_encoded]
        st.success(f"Predicted Health Status: **{prediction_label}**")

        st.subheader("📌 Personalized Recommendations:")

        # --- Caffeine Recommendations ---
        if age <= 12:
            safe_caffeine = 45
            st.markdown(
                f"**Caffeine:** For children under 12, caffeine is generally not recommended. "
                f"Safe limit is around **{safe_caffeine} mg/day** (less than half a cup of coffee). "
                f"Instead, focus on water, milk, or fresh juices. "
                f"⚠️ High caffeine can affect growth, sleep, and concentration at this age."
            )

        elif 13 <= age <= 17:
            safe_caffeine = 100
            st.markdown(
                f"**Caffeine:** For teenagers (13–17 years), keep caffeine below **{safe_caffeine} mg/day** "
                f"(about **1 small cup of coffee or 2 cups of tea**). "
                f"Excess caffeine at this stage can interfere with bone development, cause anxiety, "
                f"and disrupt sleep patterns."
            )

        elif 18 <= age <= 64:
            safe_caffeine = 400
            st.markdown(
                f"**Caffeine:** Adults can safely consume up to **{safe_caffeine} mg/day** "
                f"(roughly **3–4 regular cups of coffee**). "
                f"Consider all sources — coffee, tea, sodas, chocolate, and energy drinks. "
                f"Moderation helps improve alertness without raising risk of anxiety, dehydration, or heart strain."
            )

        else:  # 65 and above
            safe_caffeine = 250
            st.markdown(
                f"**Caffeine:** For older adults (65+), safe intake is about **{safe_caffeine} mg/day** "
                f"(around **2 cups of coffee**). "
                f"Metabolism slows with age, so excess caffeine may cause sleep issues, heart palpitations, or dehydration. "
                f"Prefer tea or decaf options in the evening."
            )

        # Warning if user exceeds safe limit
        if caffeine_mg > safe_caffeine:
            st.warning(
                f"⚠️ Your intake is **{caffeine_mg} mg/day**, which is above the safe limit of {safe_caffeine} mg/day. "
                f"Try switching to lighter brews, smaller servings, or decaf to stay within healthy range."
            )


        # --- BMI ---
        if bmi < 18.5:
            st.markdown("**BMI:** Underweight — Increase calorie intake with balanced diet, strength training.")
        elif 18.5 <= bmi <= 24.9:
            st.markdown("**BMI:** Normal weight — Maintain lifestyle, balanced diet, regular exercise.")
        elif 25 <= bmi <= 29.9:
            st.markdown("**BMI:** Overweight — Reduce calorie intake, increase physical activity, monitor weight.")
        else:
            st.markdown("**BMI:** Obese — Consult doctor/nutritionist, strict diet control, regular exercise.")

        # --- Heart Rate ---
        if heart_rate < 60:
            st.markdown("**Heart Rate:** Bradycardia (Low) — May need medical evaluation if symptomatic, maintain fitness.")
        elif 60 <= heart_rate <= 100:
            st.markdown("**Heart Rate:** Normal — Maintain healthy lifestyle, exercise regularly.")
        elif 101 <= heart_rate <= 120:
            st.markdown("**Heart Rate:** Elevated — Monitor regularly, reduce stress, improve fitness.")
        else:
            st.markdown("**Heart Rate:** Tachycardia (High) — Consult doctor, check for underlying causes, lifestyle changes.")

        # --- Stress ---
        if stress_level == "Low":
            st.markdown("**Stress:** Low — Maintain current lifestyle, continue relaxation habits, regular exercise.")
        elif stress_level == "Medium":
            st.markdown("**Stress:** Medium — Practice mindfulness, take short breaks, moderate exercise.")
        else:
            st.markdown("**Stress:** High — Consider meditation, yoga, consult professional if persistent.")

        # --- Physical Activity ---
        if physical_activity <= 1:
            st.markdown("**Physical Activity:** Low — Try at least 30 min of moderate exercise daily.")
        elif 1 < physical_activity <= 2:
            st.markdown("**Physical Activity:** Moderate — Maintain routine, include strength/flexibility exercises.")
        elif 2 < physical_activity <= 3:
            st.markdown("**Physical Activity:** Good — Keep up routine, try varied workouts for balance.")
        elif 3 < physical_activity <= 10:
            st.markdown("**Physical Activity:** Very active — Maintain activity, ensure rest and recovery.")
        else:
            st.markdown("**Physical Activity:** Extremely active — Prioritize rest, nutrition, hydration, monitor for overtraining.")

        # --- Sleep ---
        if sleep_hours < 6:
            st.markdown("**Sleep:** Less than recommended — Aim for 7–9 hrs of quality sleep. Poor sleep affects immunity and heart health.")
        elif 6 <= sleep_hours <= 9:
            st.markdown("**Sleep:** Optimal — Maintain consistent sleep schedule, avoid late caffeine/alcohol.")
        else:
            st.markdown("**Sleep:** More than 9 hrs — May indicate fatigue or low activity. Balance with exercise and routine.")

        
        # --- Smoking ---
        if smoking == "Yes":
            st.markdown("**Smoking:** Smoking increases risk of lung disease, cancer, heart problems. Strongly recommended to quit.")
        else:
            st.markdown("**Smoking:** Non-smoker — Excellent, maintain lifestyle, avoid second-hand smoke.")

        # --- Alcohol ---
        if alcohol == "Yes":
            st.markdown("**Alcohol:** Regular drinking increases risk of liver damage, heart disease, poor sleep. Reduce intake, keep alcohol-free days.")
        else:
            st.markdown("**Alcohol:** Great choice — Maintaining alcohol-free lifestyle improves long-term health.")
