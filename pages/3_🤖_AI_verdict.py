import streamlit as st
import os
from groq import Groq
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.title("🤖 AI Investment Verdict")

if "results" not in st.session_state:
    st.warning("Please calculate investment metrics on the first page.")
else:
    r = st.session_state.results
    prompt = f"""
        Given this real estate investment:
        - Price: ${r['price']}
        - Units: {r['units']}
        - Rent per unit: ${r['rent_monthly']}
        - Gross Annual Income: ${r['gross_annual']}
        - Annual Expenses: ${r['expenses_annual']}
        - Mortgage: ${r['mortgage_annual']}
        - NOI: ${r['noi']}
        - Cap Rate: {r['cap_rate']:.2f}%
        - Cash-on-Cash Return: {r['cash_on_cash']:.2f}%
        - GRM: {r['grm']:.2f}

        Please classify the investment as "Good", "Moderate", or "Poor" and give reasons Understandable and Detailed. Ensure that there is no any FONT or SPELLING mistake.
        Please respond ONLY with a JSON object in the following format:
    {{
        "verdict": "string",
        "reasons": ["reason 1", "reason 2"]
    }}
    Do not include any explanation or text outside the JSON.
    """

    if st.button("🔍 Analyze with AI"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            response = completion.choices[0].message.content.strip()

            if response.startswith("```"):
                response = re.sub(r"^```(?:json)?", "", response)
                response = re.sub(r"```$", "", response)
                response = response.strip()

            parsed = json.loads(response)
            verdict = parsed["verdict"].lower()
            if verdict == "good":
                st.success(f"✅ Verdict: {parsed['verdict']}")
            elif verdict == "moderate":
                st.warning(f"⚠️ Verdict: {parsed['verdict']}")
            elif verdict == "poor":
                st.error(f"❌ Verdict: {parsed['verdict']}")

            st.markdown("**Reasons:**")
            for reason in parsed["reasons"]:
                st.markdown(f"- {reason}")

        except Exception as e:
            st.error("❌ Failed to get AI verdict.")
            st.exception(e)
