import streamlit as st
from main2 import trip_planner

st.set_page_config(page_title="AI Trip Planner", layout="wide")

st.title("🧳 AI Trip Planner")
st.caption("Plan your entire trip using AI ✨")

with st.form("trip_form"):
    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input("From City (Code)", placeholder="DEL")
        start_date = st.date_input("Start Date")

    with col2:
        destination = st.text_input("To City (Code)", placeholder="BOM")
        end_date = st.date_input("End Date")

    submit = st.form_submit_button("🚀 Plan My Trip")

if submit:
    with st.spinner("Planning your trip..."):
        state = trip_planner.invoke({
            "origin": origin.upper(),
            "destination": destination.upper(),
            "start_date": str(start_date),
            "end_date": str(end_date),
            "travel_type": "budget"
        })

    st.success("Trip planned successfully 🎉")

    # ---------- RESULTS ----------
    st.subheader("✈️ Flights")
    st.json(state["selected_outbound_flight"])
    st.json(state["selected_return_flight"])

    st.subheader("🏨 Hotel")
    st.json(state["selected_hotel"])

    st.subheader("🌦 Weather")
    st.json(state["weather"])

    st.subheader("🍜 Local Food")
    st.write(state["local_food"])

    st.subheader("📍 Places to Visit")
    st.write(state["places_to_visit"])

    st.subheader("🕒 Best Time to Visit")
    st.json(state["best_time_to_visit"])

    st.subheader("🧾 Final Trip Summary")
    st.markdown(state["final_summary"])
