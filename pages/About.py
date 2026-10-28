# pages/About.py

import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="About | Coffee Health Risk App", layout="wide")

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: white; background: linear-gradient(to right, #9c27b0, #e91e63); 
    padding: 15px; border-radius: 10px;'>☕ Coffee Health Risk Prediction</h1>
    """,
    unsafe_allow_html=True)


# -----------------------------
# Main Title
# -----------------------------
st.markdown('<h1 style="text-align:center; color:#4B0082;">☕ Coffee Health Risk Prediction</h1>', unsafe_allow_html=True)
st.write("---")

# -----------------------------
# Problem Statement
# -----------------------------

st.markdown('<div class="highlight-title">📝 Problem Statement</div>', unsafe_allow_html=True)
st.write("""
Coffee is one of the most widely consumed beverages worldwide.  

While **moderate coffee intake** can improve alertness and mood, **excessive or irregular consumption** may cause:

- ☕ **Cardiovascular issues**: high blood pressure, rapid heart rate  
- 😴 **Sleep disorders**: insomnia, poor sleep quality  
- 😟 **Mental health challenges**: stress, anxiety, restlessness  
- ⚖️ **Metabolic effects**: BMI fluctuations, appetite changes  

Given rising global coffee consumption, a **data-driven system** is essential to predict and prevent health risks.
""")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Goals
# -----------------------------

st.markdown('<div class="highlight-title">🎯 Goals</div>', unsafe_allow_html=True)
st.write("""
- Analyze relationships between **coffee intake, caffeine levels, and lifestyle factors**  
- Predict **Health Risk Status**: 🟢 Healthy | 🟡 Mild Risk | 🔴 High Risk  
- Provide **personalized recommendations**:
  - 💪 Lifestyle (exercise, hydration, stress control)  
  - 🍎 Diet (safe caffeine levels, alternatives)  
  - 🧑‍⚕️ Medical (consultation alerts for high-risk individuals)  
- Visualize and highlight the most important factors impacting health
""")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Use Cases
# -----------------------------

st.markdown('<div class="highlight-title">💡 Use Cases</div>', unsafe_allow_html=True)
st.write("""
1. **Healthcare Advisory** – Assist doctors & nutritionists in assessing risks  
2. **Wellness Apps** – Personalized coffee intake guidance  
3. **Public Awareness** – Educates people on safe caffeine limits  
4. **Corporate Wellness Programs** – Promote healthy consumption in workplaces  
5. **Research & Policy Making** – Insights for academics and public health policies
""")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Expected Benefits
# -----------------------------

st.markdown('<div class="highlight-title">📌 Expected Benefits</div>', unsafe_allow_html=True)
st.write("""
- ✅ A **machine learning model** to predict coffee-related health risks  
- 📊 Visual insights: age, caffeine intake, and health risk patterns  
- 🧑‍⚕️ **Actionable lifestyle recommendations**  
- 🌍 Contribution to **preventive healthcare & digital health innovation**
""")
st.markdown('</div>', unsafe_allow_html=True)
