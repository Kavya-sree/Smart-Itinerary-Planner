import streamlit as st
from crewgemini.crew import run_itinerary

st.set_page_config(page_title="🛫 Smart Itinerary Planner", layout="wide")

st.markdown("""
    <style>
    /* ✅ Apply Green Style to Form Submit Button */
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #cc99ff !important; /* Green */
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: none !important;
        transition: background-color 0.3s ease-in-out !important;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #b366ff !important; /* Darker Green */
    }

    /* ✅ Blue Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFEE8C !important;
    }
    </style>
""", unsafe_allow_html=True)



st.title("🛫 Smart Itinerary Planner")
st.markdown("### Plan your trip efficiently with AI-powered recommendations! 🚀")

@st.cache_data(show_spinner=False)
def get_cached_itinerary(origin, destination, num_days, date, budget, location_preference, amenities, accommodation_type):
    return run_itinerary(origin, destination, num_days, date, budget, location_preference, amenities, accommodation_type)

# 📌 Sidebar Form for Inputs
with st.sidebar:
    st.header("📍 Trip Details")
    
    with st.form("itinerary_form"):
        origin = st.text_input("Starting Location", placeholder="e.g., New York")
        destination = st.text_input("Destination", placeholder="e.g., Paris")
        num_days = st.number_input("Number of Days", min_value=1, step=1)
        date = st.date_input("Travel Date")

        st.subheader("🏨 Accommodation Preferences")
        budget = st.selectbox("Budget Range", ["Low", "Mid-range", "Luxury"])
        location_preference = st.text_input("Preferred Location", placeholder="e.g., Near Eiffel Tower")
        amenities = st.text_area("Required Amenities", placeholder="e.g., Free WiFi, Pool, Breakfast included")
        accommodation_type = st.selectbox("Accommodation Type", ["Hotel", "Hostel", "Resort", "Vacation Rental", "Any"])

        submit_button = st.form_submit_button("🚀 Generate Itinerary") 

# 📌 Display Itinerary on the Main Page
if submit_button and origin and destination and num_days:
    if not date:
        st.error("❌ Please select a valid travel date.")
    else:
        with st.spinner("⏳ Fetching your AI-generated itinerary..."):
            try:
                itinerary = get_cached_itinerary(
                    origin, destination, num_days, date.strftime("%Y-%m-%d"),
                    budget, location_preference, amenities, accommodation_type
                )
                st.success("✅ Itinerary Generated!")

                st.markdown(f"""
                    <div class="itinerary-box">
                        <h3 style="color:#0077cc;">Your Itinerary for {destination} 📍</h3>
                        <p style="color:#333;font-size:16px;">{itinerary}</p>
                    </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Failed to generate itinerary: {str(e)}")
