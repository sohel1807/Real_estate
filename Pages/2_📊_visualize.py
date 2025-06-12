import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Visualize Investment")

if "results" not in st.session_state:
    st.warning("Please calculate values on the previous page first.")
else:
    r = st.session_state.results
    st.subheader("Choose Chart Type")
    chart_type = st.radio("Type", ["Bar Chart", "Donut Chart"])

    if chart_type == "Bar Chart":
        df = pd.DataFrame({
            "Category": ["Gross Income", "Expenses", "NOI", "Mortgage", "Cash Flow"],
            "Amount": [
                r['gross_annual'],
                r['expenses_annual'],
                r['noi'],
                r['mortgage_annual'],
                r['cashflow']
            ]
        })

        fig, ax = plt.subplots()
        ax.bar(df["Category"], df["Amount"], color=["#4CAF50", "#F44336", "#2196F3", "#FF9800", "#9C27B0"])
        ax.set_ylabel("Amount ($)")
        ax.set_title("Income & Expense Breakdown")
        st.pyplot(fig)

    elif chart_type == "Donut Chart":
        pie_labels = ["Expenses", "Mortgage", "Cash Flow"]
        pie_values = [r['expenses_annual'], r['mortgage_annual'], r['cashflow']]
        pie_colors = ["#F44336", "#FF9800", "#4CAF50"]

        fig, ax = plt.subplots()
        ax.pie(pie_values, labels=pie_labels, colors=pie_colors, startangle=90, autopct='%1.1f%%', wedgeprops=dict(width=0.3))
        ax.set_title("Income Distribution")
        st.pyplot(fig)
