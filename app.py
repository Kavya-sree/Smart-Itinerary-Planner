import streamlit as st
from crewgemini.crew import run_itinerary

# App title
st.set_page_config(page_title="Smart Itinerary Planner", layout="wide")

# Header
st.title("🛫 Smart Itinerary Planner")
st.write("Plan your trip efficiently with AI-powered recommendations!")

# Input fields
origin = st.text_input("Enter Your Starting Location", placeholder="e.g., New York")
destination = st.text_input("Enter Destination", placeholder="e.g., Paris")
date = st.date_input("Select Travel Date")

# Button to generate itinerary
if st.button("Generate Itinerary"):
    if origin and destination and date:
        with st.spinner("⏳ Fetching itinerary details..."):
            try:
                itinerary = run_itinerary(origin, destination, date.strftime("%Y-%m-%d"))
                st.success("✅ Itinerary Generated!")

                # Displaying itinerary properly
                if isinstance(itinerary, str):  
                    st.markdown(itinerary)  # Assuming text output
                elif isinstance(itinerary, dict):  
                    st.json(itinerary)  # If it's structured data
                else:
                    st.write(itinerary)

            except Exception as e:
                st.error(f"❌ Failed to generate itinerary: {str(e)}")
    else:
        st.error("⚠️ Please enter your origin, destination, and date.")
