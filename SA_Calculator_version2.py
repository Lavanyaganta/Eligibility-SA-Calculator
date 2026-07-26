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

# Reduce Spacing Between Labels & Inputs
# ------------------------------------

st.markdown("""
<style>

div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 0.2rem;
}

div[data-testid="stWidgetLabel"] {
    margin-bottom: 0rem;
}

</style>
""", unsafe_allow_html=True)



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
        Please enter customer details to calculate the <b>Indicative Eligible Sum Assured</b>.
    </p>
    """,
    unsafe_allow_html=True
)

# Reduce spacing + make labels bold
st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.4rem;
    }

    label {
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Inputs
# ------------------------------------

name = st.text_input(
    "Customer Name",
    key="name"
)
name = " ".join(name.split())

age = st.slider(
    "Age",
    min_value=0,
    max_value=100,
    value=25,
    key="age"
)


occupation = st.radio(
    "Occupation",
    ["Salaried", "Self Employed"],
    horizontal=True
)


education = st.radio(
    "Education",
    ["Graduate & Above", "HSC / 12th Pass", "10th Pass"],
    horizontal=True
)

annual_income = st.number_input(
    "Annual Income (₹)",
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
            st.stop()

        elif len(name) < 3:
            st.error("❌ Customer Name should contain at least 3 characters.")
            st.stop()

        elif not all(ch.isalpha() or ch.isspace() for ch in name):
            st.error("❌ Customer Name should contain only alphabets and spaces.")
            st.stop()

        # Age Validation

        if age < 18 or age > 60:
            st.error("❌ Age should be between 18 and 60 years.")
            st.stop()

        # Age Multiplier

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

        # ------------------------------------
        # Sum Assured Eligibility
        # ------------------------------------

        if education == "Graduate & Above":

            if occupation == "Salaried":

                if annual_income < 250000:
                    st.error("❌ Minimum income for Salaried Graduate customer is ₹2.5 Lakhs.")
                    st.stop()

                elif annual_income < 500000:
                    eligible_sa = 5000000

                else:
                    eligible_sa = annual_income * multiple

            else:

                if annual_income < 400000:
                    st.error("❌ Minimum income for Self Employed Graduate customer is ₹4 Lakhs.")
                    st.stop()

                elif annual_income < 500000:
                    eligible_sa = 5000000

                else:
                    eligible_sa = annual_income * multiple

        elif education == "HSC / 12th Pass":

            if annual_income < 500000:
                st.error("❌ Minimum income for HSC / 12th Pass customer is ₹5 Lakhs.")
                st.stop()

            eligible_sa = annual_income * multiple

        else:

            if annual_income < 1000000:
                st.error("❌ Minimum income for 10th Pass customer is ₹10 Lakhs.")
                st.stop()

            eligible_sa = annual_income * multiple

        # ------------------------------------
        # Special Case
        # ------------------------------------

        special_case = (
            education == "Graduate & Above"
            and (
                (occupation == "Salaried" and 250000 <= annual_income < 500000)
                or
                (occupation == "Self Employed" and 400000 <= annual_income < 500000)
            )
        )

        # ------------------------------------
        # Existing SA Validation
        # ------------------------------------

        if special_case:

            if existing_sa > 0:
                st.error(
                    "❌ Existing Life Cover should not be entered for customers eligible under the 'Up to ₹50 Lakhs' category."
                )
                st.stop()

        else:

            if existing_sa > eligible_sa:
                st.error(
                    "❌ Existing Sum Assured cannot exceed Eligible Sum Assured."
                )
                st.stop()

            actual_sa = max(eligible_sa - existing_sa, 0)

        # ------------------------------------
        # Results
        # ------------------------------------

        st.markdown("### Eligible Sum Assured")

        if special_case:

            st.success("Up to ₹50 Lakhs")

            st.info(
                "Final eligibility up to ₹50 Lakhs shall be subject to HDFC Life underwriting guidelines."
            )

        else:

            st.success(f"₹{indian_currency(eligible_sa)}")

            st.markdown("### Existing Life Cover")
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
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # ------------------------------------
        # Disclaimer
        # ------------------------------------

        st.markdown(
            """
            <div style="
                background-color:#F8F9FA;
                padding:20px;
                border-radius:10px;
                border:1px solid #D3D3D3;
                color:#333333;">

            <h3 style="color:#004C97;">
            📌 Disclaimer
            </h3>

            <p style="font-size:18px;font-weight:bold;color:black;">
            THIS CALCULATOR IS FOR INTERNAL USE ONLY.
            </p>

            <p>• The displayed Sum Assured is indicative only.</p>

            <p>• Final Sum Assured eligibility will be decided after Underwriting (UW) review as per HDFC Life underwriting guidelines.</p>

            <p>• Existing insurance, medical history, occupation, financial eligibility and other underwriting parameters may impact the final approval.</p>

            </div>
            """,
            unsafe_allow_html=True,
        )