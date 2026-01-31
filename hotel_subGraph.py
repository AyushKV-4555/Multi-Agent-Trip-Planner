from typing import TypedDict, Optional, List
from langgraph.graph import START
from state import TripState
import http.client, json


def fetch_hotels(state: TripState) -> TripState:
    conn = http.client.HTTPSConnection("xotelo-hotel-prices.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "6************************************",
        'x-rapidapi-host': "xotelo-hotel-prices.p.rapidapi.com"
    }

    conn.request("GET", f"/api/search?query={state['destination']}&location_type=accommodation", headers=headers)


    res = conn.getresponse()
    data = json.loads(res.read().decode())

    state["hotels"] = [
        {
            "name": h["name"],
            "place": h.get("short_place_name"),
            "url": h["url"]
        }
        for h in data["result"]["list"]
    ]

    return state

def choose_hotel(state: TripState) -> TripState:
    hotels = state.get("hotels", [])

    for i, h in enumerate(hotels[:5]):
        print(f"[{i}] {h['name']}")

    choice = input("Hotel number or skip: ").strip()

    if choice.isdigit():
        state["selected_hotel"] = hotels[int(choice)]
    else:
        state["selected_hotel"] = None

    print("✅ Hotel selected")

    return state


from langgraph.graph import StateGraph, END

hotel_graph = StateGraph(TripState)

hotel_graph.add_node("fetch_hotels", fetch_hotels)
hotel_graph.add_node("choose_hotel", choose_hotel)


hotel_graph.add_edge(START, "fetch_hotels")

hotel_graph.add_edge("fetch_hotels", "choose_hotel")
hotel_graph.add_edge("choose_hotel", END)

hotel_subgraph = hotel_graph.compile()

