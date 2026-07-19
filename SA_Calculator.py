import streamlit as st
from num2words import num2words

# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="HDFC Life SA Calculator",
    page_icon="💙",
    layout="centered"
)

# ------------------------------------
# Indian Currency Format
# ------------------------------------
def indian_currency(amount):
    amount = int(amount)
    s = str(amount)

    if len(s) <= 3:
        return s

    last_three = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return ",".join(parts) + "," + last_three

def amount_in_words(amount):
    words = num2words(int(amount), lang="en_IN").title()
    return words + " Rupees Only"


# ------------------------------------
# Heading
# ------------------------------------
st.markdown(
    """
    <h1 style="text-align:center;">
        <span style="color:#004C97;">HDFC</span>
        <span style="color:#E31837;"> LIFE</span>
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <h3 style="text-align:center; color:#333333;">
        Sum Assured Calculator
    </h3>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#5A5A5A;
        font-size:14px;
        margin-top:-10px;
        margin-bottom:20px;">
        Please enter customer details to calculate the <b>indicative Eligible Sum Assured</b>.
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ------------------------------------
# Inputs
# ------------------------------------


name = st.text_input(
    "Customer Name *",
    key="name"
)
name = " ".join(name.split())

age = st.slider(
    "Age *",
    min_value=0,
    max_value=100,
    value=25,
    key="age"
)

annual_income = st.number_input(
    "Annual Income (₹) *",
    min_value=0,
    value=0,
    step=500000,
    key="annual_income"
)

existing_sa = st.number_input(
    "Existing Sum Assured (₹) (If Applicable)",
    min_value=0,
    value=0,
    step=500000,
    key="existing_sa"
)

st.markdown("---")

# ------------------------------------
# Clear Function
# ------------------------------------
def clear_fields():
    st.session_state["name"] = ""
    st.session_state["age"] = 25
    st.session_state["annual_income"] = 0
    st.session_state["existing_sa"] = 0

# ------------------------------------
# Buttons
# ------------------------------------

col1, col2 = st.columns(2)

with col1:
    calculate = st.button("Calculate SA")

with col2:
    st.button("Clear", on_click=clear_fields)


# ------------------------------------
# Calculation
# ------------------------------------
if calculate:

    with st.spinner("Calculating Eligible Sum Assured..."):

        # Customer Name Validation
        if not name.strip():
            st.warning("⚠ Please enter Customer Name.")

        elif len(name) < 3:
            st.error("❌ Customer Name should contain at least 3 characters.")

        elif not all(ch.isalpha() or ch.isspace() for ch in name):
            st.error("❌ Customer Name should contain only alphabets and spaces.")

        # Age Validation
        elif age < 18 or age > 60:
            st.error("❌ Age should be between 18 and 60 years.")

        # Income Validation
        elif annual_income < 500000:
            st.error(
                "❌ Customer is not eligible.\n\n"
                "Minimum Annual Income should be at least ₹5,00,000."
            )

        else:

            # Income Multiple
            if age <= 30:
                multiple = 35
            elif age <= 35:
                multiple = 30
            elif age <= 40:
                multiple = 25
            elif age <= 45:
                multiple = 20
            elif age <= 50:
                multiple = 15
            elif age <= 55:
                multiple = 10
            else:
                multiple = 5

            # Eligible Sum Assured
            eligible_sa = annual_income * multiple

            # Existing SA Validation
            if existing_sa > eligible_sa:
                st.error("❌ Existing Sum Assured cannot exceed Eligible Sum Assured.")

            else:
                actual_sa = eligible_sa - existing_sa

                st.markdown("### Eligible Sum Assured")
                st.success(f"₹{indian_currency(eligible_sa)}")

                st.markdown("### Existing Life Cover (₹)")
                st.info(f"₹{indian_currency(existing_sa)}")

                st.markdown("### Final Eligible Sum Assured")
                st.success(f"₹{indian_currency(actual_sa)}")

                st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#666666;
        font-size:16px;
        font-style:italic;
        margin-top:-8px;
        margin-bottom:12px;">
        {amount_in_words(actual_sa)}
    </div>
    """,
    unsafe_allow_html=True
)

                st.markdown("---")

                st.markdown(
    """
    <div style="
        background-color:#F8F9FA;
        padding:20px;
        border-radius:10px;
        border:1px solid #D3D3D3
        color:#333333;">

    <h3 style="color:#004C97; margin-bottom:20px;">
    📌 Disclaimer
    </h3>

    <p style="font-size:18px; font-weight:bold; color:black;">
    THIS CALCULATOR IS FOR INTERNAL USE ONLY.
    </p>

    <p>
    • The displayed Sum Assured is indicative only.
    </p>

    <p>
    • Final Sum Assured eligibility will be decided after Underwriting (UW) review as per HDFC Life underwriting guidelines.
    </p>

    <p>
    • Existing insurance, medical history, occupation, financial eligibility and other underwriting parameters may impact the final approval.
    </p>


    </div>
    """,
    unsafe_allow_html=True
)

 