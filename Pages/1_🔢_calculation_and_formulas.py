import streamlit as st

st.title("📋 Investment Calculator")

col1, col2 = st.columns(2)
with col1:
    price = st.number_input("Purchase Price ($)", value=500000, step=10000)
    sqft = st.number_input("Total Square Footage", value=1500, step=50)
    units = st.number_input("Number of Units", min_value=1, value=2)
    age = st.number_input("Building Age (years)", value=10)

with col2:
    rent_monthly = st.number_input("Monthly Rent per Unit ($)", value=12000, step=500)
    expenses_annual = st.number_input("Annual Expenses ($)", value=50000, step=1000)
    down_payment = st.number_input("Down Payment ($)", value=100000, step=5000)
    mortgage_annual = st.number_input("Annual Mortgage Payment ($)", value=0)

if st.button("📊 Calculate"):
    gross_monthly = units * rent_monthly
    gross_annual = gross_monthly * 12
    noi = gross_annual - expenses_annual
    cap_rate = (noi / price) * 100 if price else 0
    annual_cash_flow = noi - mortgage_annual
    cash_on_cash = (annual_cash_flow / down_payment) * 100 if down_payment else 0
    grm = price / gross_annual if gross_annual else 0

    st.session_state.results = {
    "price": price,
    "units": units,
    "rent_monthly": rent_monthly,
    "gross_monthly": gross_monthly,  
    "gross_annual": gross_annual,
    "expenses_annual": expenses_annual,
    "mortgage_annual": mortgage_annual,
    "noi": noi,
    "cap_rate": cap_rate,
    "cashflow": annual_cash_flow,
    "cash_on_cash": cash_on_cash,
    "grm": grm
}


if "results" in st.session_state and st.session_state.results:
    r = st.session_state.results

    st.subheader("📈 Investment Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Income", f"${r['gross_monthly']:,.0f}")
    col2.metric("NOI", f"${r['noi']:,.0f}")
    col3.metric("Cap Rate", f"{r['cap_rate']:.2f}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("Annual Cash Flow", f"${r['cashflow']:,.0f}")
    col5.metric("Cash-on-Cash", f"{r['cash_on_cash']:.2f}%")
    col6.metric("GRM", f"{r['grm']:.2f}")

    with st.expander("📘 Formula Breakdown"):
        st.markdown(f"""
        - **Gross Monthly Income =** Units × Rent = {units} × ${rent_monthly} = ${r['gross_monthly']}
        - **Gross Annual Income =** ${r['gross_monthly']} × 12 = ${r['gross_annual']}
        - **NOI =** Gross Annual – Expenses = ${r['gross_annual']} – ${expenses_annual} = ${r['noi']}
        - **Cap Rate =** (NOI ÷ Price) × 100 = ({r['noi']} ÷ {price}) × 100 = {r['cap_rate']:.2f}%
        - **Cash-on-Cash =** (Annual Cash Flow ÷ Down Payment) × 100 = ({r['cashflow']} ÷ {down_payment}) × 100 = {r['cash_on_cash']:.2f}%
        - **GRM =** Price ÷ Gross Annual Income = {price} ÷ {r['gross_annual']} = {r['grm']:.2f}
        """)
