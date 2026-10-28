# pages/Model.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import warnings
warnings.filterwarnings("ignore")

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay
)
from sklearn.model_selection import StratifiedKFold, cross_validate, GridSearchCV
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE

st.set_page_config(page_title="Coffee Health Risk - Model", layout="wide")
st.title("☕ Coffee Health Risk Prediction - Model Page")
st.markdown("This page demonstrates the **training, evaluation, and tuning** of the Decision Tree pipeline using SMOTE for handling imbalanced target classes.")

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean_coffee_dataset .csv")  # Replace with your file path
    return df

df = load_data()
st.subheader("Dataset Overview")
st.dataframe(df.head())
st.write("Target column counts:")
st.bar_chart(df['Health_Status'].value_counts())

# -----------------------------
# Preprocessing
# -----------------------------
st.subheader("Preprocessing & Pipeline Setup")

num_cols = ['Age','Coffee_Intake_Cups','Caffeine_mg','Sleep_Hours','BMI','Heart_Rate','Physical_Activity_Hours']
cat_one = ['Gender','Occupation','Coffee_Type']
cat_ord = ['Sleep_Quality','Stress_Level']

Sleep_Quality_order = ['Poor','Fair','Good','Excellent']
Stress_Level_order = ['Low', 'Medium', 'High']

ct = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('one', OneHotEncoder(sparse_output=False, handle_unknown='ignore'), cat_one),
    ('ord', OrdinalEncoder(categories=[Sleep_Quality_order, Stress_Level_order]), cat_ord)
], remainder='passthrough', verbose_feature_names_out=False, force_int_remainder_cols=True).set_output(transform='pandas')

# Target mapping
mapping = {'Healthy':0, 'Mild Risk':1, 'High Risk':2}
reverse_mapping = {v:k for k,v in mapping.items()}

X = df.drop(columns=['ID','Health_Status','Country'], axis=1)
y = df[['Health_Status']]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

y_train_encoded = y_train.squeeze().map(mapping)
y_test_encoded = y_test.squeeze().map(mapping)

# Pipeline with SMOTE + Decision Tree
pipeline = ImbPipeline(steps=[
    ("preprocessor", ct),
    ("smote", SMOTE(random_state=42)),
    ("classifier", DecisionTreeClassifier(random_state=42))
])

st.write("Pipeline successfully created with SMOTE and Decision Tree classifier.")

# -----------------------------
# Train Pipeline
# -----------------------------
st.subheader("Training Pipeline")
pipeline.fit(X_train, y_train_encoded)
st.write(f"Train Accuracy: {pipeline.score(X_train, y_train_encoded):.4f}")
st.write(f"Test Accuracy: {pipeline.score(X_test, y_test_encoded):.4f}")

# -----------------------------
# Cross-validation
# -----------------------------
st.subheader("Cross-validation Results")
scoring = ['accuracy','precision_macro','recall_macro','f1_macro']
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_results = cross_validate(
    pipeline, X_train, y_train_encoded,
    cv=cv, scoring=scoring, return_train_score=True, n_jobs=-1
)

for metric in scoring:
    train_mean = cv_results[f'train_{metric}'].mean()
    test_mean = cv_results[f'test_{metric}'].mean()
    st.write(f"{metric}: train={train_mean:.4f}, val={test_mean:.4f}")

# -----------------------------
# Test set evaluation
# -----------------------------
st.subheader("Test Set Evaluation")
y_pred = pipeline.predict(X_test)

st.write(f"Accuracy: {accuracy_score(y_test_encoded, y_pred):.4f}")
st.write(f"Precision: {precision_score(y_test_encoded, y_pred, average='macro'):.4f}")
st.write(f"Recall: {recall_score(y_test_encoded, y_pred, average='macro'):.4f}")
st.write(f"F1-score: {f1_score(y_test_encoded, y_pred, average='macro'):.4f}")

st.text("Classification Report:")
st.text(classification_report(
    y_test_encoded, y_pred, target_names=[reverse_mapping[i] for i in sorted(reverse_mapping.keys())]
))

cm = confusion_matrix(y_test_encoded, y_pred)
st.text("Confusion Matrix:")
fig, ax = plt.subplots(figsize=(6,6))
disp = ConfusionMatrixDisplay(cm, display_labels=[reverse_mapping[i] for i in sorted(reverse_mapping.keys())])
disp.plot(ax=ax, cmap='Blues', values_format='d')
st.pyplot(fig)

# -----------------------------
# Decision Tree Visualization
# -----------------------------
st.subheader("Decision Tree Visualization")
def get_feature_names_from_column_transformer(ct):
    try:
        names = ct.get_feature_names_out()
        return list(map(str, names))
    except:
        feature_names = []
        for name, transformer, columns in ct.transformers_:
            if name=='remainder' or transformer=='drop':
                continue
            try:
                trans_feature_names = transformer.get_feature_names_out(columns)
                feature_names.extend(list(map(str, trans_feature_names)))
            except:
                if isinstance(columns,(list,tuple,np.ndarray)):
                    feature_names.extend(list(map(str, columns)))
                else:
                    feature_names.append(str(columns))
        return feature_names

dt_model = pipeline.named_steps["classifier"]
feature_names = get_feature_names_from_column_transformer(ct)

fig, ax = plt.subplots(figsize=(20,12))
plot_tree(
    dt_model,
    feature_names=feature_names,
    class_names=[reverse_mapping[i] for i in sorted(reverse_mapping.keys())],
    filled=True, rounded=True, fontsize=10
)
st.pyplot(fig)

# -----------------------------
# Feature Importances
# -----------------------------
st.subheader("Top Feature Importances")
importances = dt_model.feature_importances_
feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
st.dataframe(feat_imp.head(20))

fig, ax = plt.subplots(figsize=(8,6))
feat_imp.head(20).plot.barh(ax=ax)
ax.invert_yaxis()
ax.set_title("Top Feature Importances (Decision Tree)")
plt.tight_layout()
st.pyplot(fig)

# -----------------------------
# Hyperparameter Tuning
# -----------------------------
st.subheader("Hyperparameter Tuning (GridSearchCV)")
param_grid = {
    "classifier__max_depth": [None,5,8,12],
    "classifier__min_samples_split": [2,5,10],
    "classifier__min_samples_leaf": [1,2,4],
    "classifier__criterion": ["gini","entropy"]
}

gs = GridSearchCV(
    estimator=pipeline,
    param_grid=param_grid,
    scoring='f1_macro',
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    n_jobs=-1,
    verbose=1,
    return_train_score=True
)
gs.fit(X_train, y_train_encoded)
best_pipeline = gs.best_estimator_
st.write("Best parameters:", gs.best_params_)
st.write("Best CV f1_macro:", gs.best_score_)

# -----------------------------
# Save Pipeline + Mapping
# -----------------------------
save_obj = {"model": best_pipeline, "target_mapping": mapping, "reverse_mapping": reverse_mapping}
with open("coffee_health_best_pipeline.pkl", "wb") as f:
    pickle.dump(save_obj, f)
st.success("✅ Saved best pipeline to 'coffee_health_best_pipeline.pkl'")
