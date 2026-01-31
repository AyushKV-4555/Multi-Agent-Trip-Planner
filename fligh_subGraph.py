from typing import TypedDict, Optional, List

from state import TripState
import http.client
import json
import os

def fetch_flights(state: TripState) -> TripState:
    conn = http.client.HTTPSConnection("flight-fare-search.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": "***************************************",
        "x-rapidapi-host": "flight-fare-search.p.rapidapi.com"
    }

    conn.request("GET", f"/v2/flights/?from={state['origin']}&to={state['destination']}&date={state['start_date']}&adult=1&type=economy&currency=USD", headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode())

    state["outbound_flights"] = data.get("results", [])
    return state


def shortlist_flights(state: TripState) -> TripState:
    flights = state["outbound_flights"]

    if not flights:
        print("❌ No flights found")
        return state

    if state["travel_type"] == "budget":
        flights = sorted(flights, key=lambda x: x["totals"]["total"])
    else:
        flights = sorted(
            flights,
            key=lambda x: (x["duration"]["value"], -x["totals"]["total"])
        )

    state["outbound_flights"] = flights[:5]
    return state


def select_flight(state: TripState) -> TripState:
    flights = state["outbound_flights"]

    for i, f in enumerate(flights):
        print(f"[{i}] {f['flight_name']} | {round(f['totals']['total'])} USD")

    while True:
        choice = input("Select flight: ").strip()
        if choice.isdigit() and int(choice) < len(flights):
            state["selected_outbound_flight"] = flights[int(choice)]
            print("✅ Flight selected")
            return state

from langgraph.graph import StateGraph, END, START

flight_graph = StateGraph(TripState)

flight_graph.add_edge(START, "fetch")
flight_graph.add_node("fetch", fetch_flights)
flight_graph.add_node("shortlist", shortlist_flights)
flight_graph.add_node("select", select_flight)

flight_graph.add_edge("fetch", "shortlist")
flight_graph.add_edge("shortlist", "select")
flight_graph.add_edge("select", END)

flight_subgraph = flight_graph.compile()

