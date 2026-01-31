from typing import TypedDict, Optional, Dict
from state import TripState
    
import requests

API_KEY = "5*******************************"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def fetch_weather(state: TripState) -> TripState:
    city = state["destination"]

    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    state["weather"] = {
        "temp": data["main"]["temp"],
        "desc": data["weather"][0]["description"]
    }

    return state


from langgraph.graph import StateGraph, START, END

weather_graph = StateGraph(TripState)

weather_graph.add_node("fetch_weather", fetch_weather)

# ✅ REQUIRED entrypoint
weather_graph.add_edge(START, "fetch_weather")
weather_graph.add_edge("fetch_weather", END)

weather_subgraph = weather_graph.compile()
