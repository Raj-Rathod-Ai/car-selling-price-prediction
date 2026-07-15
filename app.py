import streamlit as st
import utils
import datetime

# Page configuration
st.set_page_config(
    page_title="Car Value Estimator",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for SaaS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .saas-card {
        background: padding-box;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 2rem;
    }
    
    .progress-wrapper {
        margin-bottom: 2rem;
    }
    .progress-text {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #3B82F6;
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .question-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #1E293B;
    }
    .question-desc {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.2s ease-in-out;
    }
    
    @media (prefers-color-scheme: dark) {
        .question-title {
            color: #F8FAFC;
        }
        .question-desc {
            color: #94A3B8;
        }
    }
</style>
""", unsafe_html=True)

# Initialize Session State
if "step" not in st.session_state:
    st.session_state.step = 1

# Answer stores
if "car_name" not in st.session_state:
    st.session_state.car_name = utils.CAR_NAMES[0]

current_year = datetime.datetime.now().year
if "year" not in st.session_state:
    st.session_state.year = utils.DEFAULTS['Year']

if "present_price" not in st.session_state:
    st.session_state.present_price = float(utils.DEFAULTS['Present_Price'])
if "present_price_known" not in st.session_state:
    st.session_state.present_price_known = True

if "kms_driven" not in st.session_state:
    st.session_state.kms_driven = int(utils.DEFAULTS['Kms_Driven'])

if "fuel_type" not in st.session_state:
    st.session_state.fuel_type = "Petrol"

if "seller_type" not in st.session_state:
    st.session_state.seller_type = "Individual"

if "transmission" not in st.session_state:
    st.session_state.transmission = "Manual"

if "owner" not in st.session_state:
    st.session_state.owner = 0

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

def reset_wizard():
    st.session_state.step = 1
    st.session_state.car_name = utils.CAR_NAMES[0]
    st.session_state.year = utils.DEFAULTS['Year']
    st.session_state.present_price = float(utils.DEFAULTS['Present_Price'])
    st.session_state.present_price_known = True
    st.session_state.kms_driven = int(utils.DEFAULTS['Kms_Driven'])
    st.session_state.fuel_type = "Petrol"
    st.session_state.seller_type = "Individual"
    st.session_state.transmission = "Manual"
    st.session_state.owner = 0

st.title("🚗 Car Value Estimator")
st.markdown("Find out the estimated market price for selling your pre-owned car.")

TOTAL_STEPS = 9
progress_percentage = int((st.session_state.step - 1) / TOTAL_STEPS * 100)

# Render Progress Bar
st.markdown(f"""
<div class="progress-wrapper">
    <div class="progress-text">
        <span>Question {min(st.session_state.step, TOTAL_STEPS)} of {TOTAL_STEPS}</span>
        <span>{progress_percentage}% Complete</span>
    </div>
</div>
""", unsafe_html=True)
st.progress(progress_percentage / 100.0)

st.markdown('<div class="saas-card">', unsafe_html=True)

if st.session_state.step == 1:
    st.markdown('<div class="question-title">Step 1: Car Model</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">Which manufacturer and model is your car?</div>', unsafe_html=True)
    
    # Capitalize model name for display
    car_name = st.selectbox(
        "Car Model / Name",
        options=utils.CAR_NAMES,
        index=utils.CAR_NAMES.index(st.session_state.car_name)
    )
    st.session_state.car_name = car_name
    
    col1, col2 = st.columns([1, 4])
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 2:
    st.markdown('<div class="question-title">Step 2: Manufacturing Year</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">In which year was your car manufactured?</div>', unsafe_html=True)
    
    year = st.number_input(
        "Year of Manufacture",
        min_value=1990,
        max_value=current_year,
        value=st.session_state.year,
        step=1
    )
    st.session_state.year = year
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 3:
    st.markdown('<div class="question-title">Step 3: Original Showroom Price</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">What is/was the showroom price of a brand-new car of this model (in Lakhs, e.g. 5.5 Lakhs is ~550,000 INR)?</div>', unsafe_html=True)
    
    known = st.checkbox("I know the showroom price", value=st.session_state.present_price_known)
    st.session_state.present_price_known = known
    
    if known:
        price = st.number_input(
            "Showroom Price (Lakhs)",
            min_value=0.1,
            max_value=150.0,
            value=st.session_state.present_price if st.session_state.present_price is not None else utils.DEFAULTS['Present_Price'],
            step=0.1
        )
        st.session_state.present_price = price
    else:
        st.info(f"Using default model showroom price: **{utils.DEFAULTS['Present_Price']:.2f} Lakhs**")
        st.session_state.present_price = None
        
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 4:
    st.markdown('<div class="question-title">Step 4: Mileage / Kilometers Driven</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">How many total kilometers has your car been driven?</div>', unsafe_html=True)
    
    kms = st.number_input(
        "Total Kilometers Driven",
        min_value=0,
        max_value=1000000,
        value=st.session_state.kms_driven,
        step=1000
    )
    st.session_state.kms_driven = kms
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 5:
    st.markdown('<div class="question-title">Step 5: Fuel Type</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">What type of fuel does your car consume?</div>', unsafe_html=True)
    
    fuels = list(utils.FUEL_MAPPING.keys())
    fuel = st.selectbox(
        "Fuel Type",
        options=fuels,
        index=fuels.index(st.session_state.fuel_type)
    )
    st.session_state.fuel_type = fuel
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 6:
    st.markdown('<div class="question-title">Step 6: Seller Type</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">Are you selling as an individual owner, or through a dealer?</div>', unsafe_html=True)
    
    sellers = list(utils.SELLER_MAPPING.keys())
    seller = st.selectbox(
        "Seller Type",
        options=sellers,
        index=sellers.index(st.session_state.seller_type)
    )
    st.session_state.seller_type = seller
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 7:
    st.markdown('<div class="question-title">Step 7: Transmission Type</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">What transmission type does your car have?</div>', unsafe_html=True)
    
    trans_options = list(utils.TRANSMISSION_MAPPING.keys())
    trans = st.selectbox(
        "Transmission",
        options=trans_options,
        index=trans_options.index(st.session_state.transmission)
    )
    st.session_state.transmission = trans
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Next Question →", on_click=next_step, type="primary")

elif st.session_state.step == 8:
    st.markdown('<div class="question-title">Step 8: Number of Previous Owners</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">How many previous owners has this car had before you?</div>', unsafe_html=True)
    
    owner = st.selectbox(
        "Previous Owners",
        options=[0, 1, 2, 3],
        index=st.session_state.owner
    )
    st.session_state.owner = owner
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        st.button("Review Summary →", on_click=next_step, type="primary")

elif st.session_state.step == 9:
    st.markdown('<div class="question-title">Summary of Answers</div>', unsafe_html=True)
    st.markdown('<div class="question-desc">Review your car details before generating the selling value prediction.</div>', unsafe_html=True)
    
    show_price = f"{st.session_state.present_price:.2f} Lakhs" if st.session_state.present_price_known else "Unknown (using standard average)"
    
    st.markdown(f"""
    | Car Detail | Your Answer |
    | :--- | :--- |
    | **Car Model** | {st.session_state.car_name.upper()} |
    | **Manufacturing Year** | {st.session_state.year} |
    | **Original Showroom Price** | {show_price} |
    | **Kilometers Driven** | {st.session_state.kms_driven:,} km |
    | **Fuel Type** | {st.session_state.fuel_type} |
    | **Seller Type** | {st.session_state.seller_type} |
    | **Transmission** | {st.session_state.transmission} |
    | **Previous Owners** | {st.session_state.owner} |
    """, unsafe_html=True)
    
    st.write("")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("← Back", on_click=prev_step)
    with col2:
        predict_clicked = st.button("💰 Predict Selling Price", type="primary")
        
    if predict_clicked:
        try:
            with st.spinner("Calculating estimated selling price..."):
                est_price = utils.predict_selling_price(
                    st.session_state.car_name,
                    st.session_state.year,
                    st.session_state.present_price,
                    st.session_state.kms_driven,
                    st.session_state.fuel_type,
                    st.session_state.seller_type,
                    st.session_state.transmission,
                    st.session_state.owner
                )
            
            # Format and display price
            st.write("")
            st.markdown(f"""
            <div style="background: rgba(59, 130, 246, 0.1); border-left: 5px solid #3B82F6; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
                <h4 style="color: #3B82F6; margin: 0 0 0.5rem 0;">Estimated Selling Value</h4>
                <p style="font-size: 2.2rem; font-weight: 700; color: #1D4ED8; margin: 0;">{est_price:.2f} Lakhs</p>
                <p style="font-size: 0.95rem; color: #1E40AF; margin: 0.5rem 0 0 0; line-height: 1.5;">
                    This represents the estimated price (in Lakhs) you could sell your car for on the pre-owned market, based on its age, showroom price, odometer reading, fuel type, transmission, and owner count.
                </p>
            </div>
            """, unsafe_html=True)
            st.balloons()
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            
    st.write("")
    st.button("🔄 Restart Assessment", on_click=reset_wizard)

st.markdown('</div>', unsafe_html=True)
