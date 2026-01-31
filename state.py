from typing import TypedDict, Optional, Dict, Any, List


class TripState(TypedDict, total=False):
    # User input
    origin: str
    destination: str
    start_date: str
    end_date: str
    travel_type: str  # budget | expensive

    # Flights
    outbound_flights: List[Dict[str, Any]]
    selected_outbound_flight: Optional[Dict[str, Any]]

    return_flights: List[Dict[str, Any]]
    selected_return_flight: Optional[Dict[str, Any]]

    # Hotels
    hotels: List[Dict[str, Any]]
    selected_hotel: Optional[Dict[str, Any]]

    # Weather
    weather: Optional[Dict[str, Any]]

    # LLM recommendations
    local_food: Optional[str]
    places_to_visit: Optional[str]
    best_time_to_visit: Optional[str]

    stage: str