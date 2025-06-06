import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Investor Profiling Form", layout="centered")

st.title("📋 Investor Profiling Form")

# 📁 File path to save data
file_path = "data.xlsx"

# Load existing data if file exists
if os.path.exists(file_path):
    df_existing = pd.read_excel(file_path)
else:
    df_existing = pd.DataFrame()

# ------------------------- FORM ------------------------- #

with st.form("investor_form"):
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    occupation = st.selectbox(
        "Occupation",
        ["Salaried", "Business", "HNI", "Retired", "Student", "Freelancer", "Other"]
    )
    income = st.number_input("Monthly Income (₹)", step=1000)
    fixed_exp = st.number_input("Fixed Expenses (₹)", step=1000)
    variable_exp = st.number_input("Variable Expenses (₹)", step=1000)
    
    risk = st.radio("Risk Appetite", ["Conservative", "Moderate", "Aggressive"])
    
    goals = st.multiselect(
        "Select Your Financial Goals",
        ["House", "Car", "Child Education", "Retirement", "Legacy Planning", "Second Home", "Travel", "Other"]
    )
    custom_goal = st.text_input("Other Goal (if any)")
    
    savings = st.number_input("Total Savings (₹)", step=10000)
    investments = st.number_input("Total Investments (₹)", step=10000)
    
    submitted = st.form_submit_button("Submit")

# --------------------- SCORING LOGIC --------------------- #

def calculate_score(risk, income, savings, investments):
    score = 0
    
    # Risk preference
    if risk == "Conservative":
        score += 1
    elif risk == "Moderate":
        score += 2
    elif risk == "Aggressive":
        score += 3

    # Financial strength (very basic logic)
    if income > 100000:
        score += 2
    elif income > 50000:
        score += 1

    if savings > 500000:
        score += 2
    elif savings > 100000:
        score += 1

    if investments > 1000000:
        score += 2
    elif investments > 500000:
        score += 1

    return score

def classify_investor(score):
    if score <= 3:
        return "Conservative"
    elif score <= 6:
        return "Moderate"
    else:
        return "Aggressive"

# -------------------- DATA STORAGE -------------------- #

if submitted:
    full_goals = goals.copy()
    if custom_goal:
        full_goals.append(custom_goal)
    
    score = calculate_score(risk, income, savings, investments)
    investor_type = classify_investor(score)

    # Prepare new entry
    new_data = {
        "Name": name,
        "Age": age,
        "Occupation": occupation,
        "Income": income,
        "Fixed Exp": fixed_exp,
        "Variable Exp": variable_exp,
        "Risk": risk,
        "Goals": ", ".join(full_goals),
        "Savings": savings,
        "Investments": investments,
        "Score": score,
        "Investor Type": investor_type
    }

    # Append to existing data
    df_combined = pd.concat([df_existing, pd.DataFrame([new_data])], ignore_index=True)
    df_combined.to_excel(file_path, index=False)

    st.success("Thank you! Your response has been recorded.")

