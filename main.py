
from fligh_subGraph import flight_subgraph
from hotel_subGraph import hotel_subgraph
from weather_subGraph import weather_subgraph
from state import TripState
import os
from langchain_groq import ChatGroq
from store import FLIGHT_STORE, HOTEL_STORE

os.environ["GROQ_API_KEY"] = "****************************"

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3
)

import json
import re

def extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def user_input_node(state: TripState) -> TripState:
    print("\n🧳 AI Trip Planner")


    state["origin"] = input(
    "From city (e.g. DEL – Delhi, BOM – Mumbai, BLR – Bengaluru): ").title()

    state["destination"] = input(
        "To city (e.g. CCU – Kolkata, HYD – Hyderabad, MAA – Chennai): ").title()

    state["start_date"] = input("Start date (YYYY-MM-DD): ")
    state["end_date"] = input("End date (YYYY-MM-DD): ")

    return state

from store import FLIGHT_STORE

def outbound_flight_node(state: TripState) -> TripState:
    print("\n✈️ Fetching outbound flights...")

    state["travel_type"] = "budget"

    source = state["origin"]
    destination = state["destination"]

    route_key = f"{source}_{destination}"

    # 🔍 Step 1: Check local store
    if route_key in FLIGHT_STORE:
        print("🟢 Using stored flight data (no API call)")
        flights = FLIGHT_STORE[route_key]
        print("There are some flights available: \n")
        for i, f in enumerate(flights):
            print(
                f"[{i}] {f.get('airline', 'Unknown')} "
                f"{f.get('flight_no', '')} | "
                f"{round(f['totals']['total'])} INR"
            )
        user_input = input("Should i finalaize it? (y/n): ").strip()
        state["outbound_flights"] = FLIGHT_STORE[route_key]
        if user_input.lower() == "y":
            state["selected_outbound_flight"] = FLIGHT_STORE[route_key][0]
            print('✅ flight booking done')
            return state

    # 🌐 Step 2: Call paid API ONLY if data not found
    print("🔵 Calling flight API...")
    state = flight_subgraph.invoke(state)

    # 💾 Step 3: Store result for future use
    if state.get("outbound_flights"):
        FLIGHT_STORE[route_key] = state["outbound_flights"]

    return state


def return_flight_node(state: TripState) -> TripState:
    print("\n✈️ Fetching return flights...")

    source = state["destination"]
    destination = state["origin"]

    route_key = f"{source}_{destination}"
    
    # 🔍 Step 1: Check local store
    if route_key in FLIGHT_STORE:
        print("🟢 Using stored flight data (no API call)")
        flights = FLIGHT_STORE[route_key]
        print("There are some flights available: \n")
        for i, f in enumerate(flights):
            print(
                f"[{i}] {f.get('airline', 'Unknown')} "
                f"{f.get('flight_no', '')} | "
                f"{round(f['totals']['total'])} INR"
            )
        user_input = input("Should i finalaize it? (y/n): ").strip()
        state["return_flights"] = FLIGHT_STORE[route_key]
        if user_input.lower() == "y":
            state["selected_return_flight"] = FLIGHT_STORE[route_key][0]
            print('✅ return flight booking done')
            return state

    result = flight_subgraph.invoke({
        "origin": source,
        "destination": destination,
        "travel_type": state["travel_type"]
    })

    state["return_flights"] = result["outbound_flights"]
    state["selected_return_flight"] = result["selected_outbound_flight"]

    return state

def hotel_node(state: TripState) -> TripState:
    print("\n🏨 Fetching hotels...")
    city = state["destination"]
    
    if city in HOTEL_STORE:
        print("🟢 Using stored flight data")
        hotel = HOTEL_STORE[city]
        state["hotels"] = hotel
        print("There are some flights available: \n")
        for i, f in enumerate(hotel):
            print(
                f"[{i}] {f.get('name', 'Unknown')} "
                f"{f.get('place', '')} | "
                f"{f.get('url')}"
            )
        user_input = int(input("Select which one finalaize: "))
        state["selected_hotel"] = HOTEL_STORE[city][user_input]
        print('✅ return flight booking done')
        return state

    result = hotel_subgraph.invoke(state)

    state["hotels"] = result["hotels"]
    state["selected_hotel"] = result.get("selected_hotel")

    return state

def weather_node(state):
    print("🌦 Fetching weather...")
    state = weather_subgraph.invoke(state)
    print("✅ Weather fetched")
    return state


def llm_recommendation_node(state: TripState) -> TripState:
    city = state["destination"]

    prompt = f"""
    You are a travel expert.
    Destination: {city}

    Return ONLY valid JSON. No text. No markdown.

    {{
        "local_food": ["food1", "food2", "food3"],
        "places_to_visit": ["place1", "place2", "place3"],
        "best_time_to_visit": {{
            "season": "best season",
            "time_of_day": "best time of day"
        }}
    }}
    """

    resp = llm.invoke(prompt)

    try:
        data = extract_json(resp.content)

        state["local_food"] = data.get("local_food", [])
        state["places_to_visit"] = data.get("places_to_visit", [])
        state["best_time_to_visit"] = data.get("best_time_to_visit", {})

        print("✅ Travel recommendations generated")

    except Exception as e:
        print("❌ LLM JSON parse failed:", e)
        state["llm_raw_response"] = resp.content

    return state

def final_summary_node(state: TripState) -> TripState:
    summary_input = {
        "outbound_flight": state.get("selected_outbound_flight"),
        "hotel": state.get("selected_hotel"),
        "weather": state.get("weather"),
        "recommendations": {
            "local_food": state.get("local_food", []),
            "places_to_visit": state.get("places_to_visit", []),
            "best_time_to_visit": state.get("best_time_to_visit", {})
        },
        "return_flight": state.get("selected_return_flight")
    }

    prompt = f"""
    You are a travel planner.

    Using the data below, generate a clean, user-friendly trip summary.
    Keep it concise and well-formatted.

    DATA:
    {json.dumps(summary_input, indent=2)}
    """

    resp = llm.invoke(prompt)

    print("\n🧾 FINAL TRIP PLAN\n")
    print(resp.content)

    return state


from langgraph.graph import StateGraph, START, END

graph = StateGraph(TripState)

graph.add_node("input", user_input_node)
graph.add_node("out_flight", outbound_flight_node)
graph.add_node("hotel", hotel_node)
graph.add_node("weather", weather_node)
graph.add_node("llm", llm_recommendation_node)
graph.add_node("return_flight", return_flight_node)
graph.add_node("final", final_summary_node)

graph.add_edge(START, "input")
graph.add_edge("input", "out_flight")
graph.add_edge("out_flight", "hotel")
graph.add_edge("hotel", "weather")
graph.add_edge("weather", "llm")
graph.add_edge("llm", "return_flight")
graph.add_edge("return_flight", "final")
graph.add_edge("final", END)

trip_planner = graph.compile()

trip_planner.invoke({
    "travel_type":'budget'
})