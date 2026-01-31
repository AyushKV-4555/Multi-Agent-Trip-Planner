# AI Trip Planner


### High-Level Architecture (Agent View)

                Root Graph (Trip Planner Orchestrator)
                │
                ├── User Input Node
                │     ├─ origin
                │     ├─ destination
                │     ├─ start_date
                │     └─ end_date
                │
                ├── Outbound Flight SubGraph
                │     ├─ Fetch Flights
                │     ├─ Rank Flights (budget / fastest / best)
                │     └─ Select Outbound Flight
                │
                ├── Decision Router (User Choice Loop)
                │     ├─ Hotel Flow (optional)
                │     ├─ Weather Flow (optional)
                │     ├─ Travel Intelligence (LLM)
                │     ├─ Return Flight Flow
                │     └─ Final Summary
                │
                ├── Hotel SubGraph (Optional)
                │     ├─ Fetch Hotels
                │     ├─ Display Options
                │     └─ Select Hotel
                │
                ├── Weather SubGraph (Optional)
                │     ├─ Fetch Weather
                │     └─ Normalize Forecast
                │
                ├── Travel Intelligence Node (LLM)
                │     ├─ Famous Local Food
                │     ├─ Places to Visit
                │     ├─ Best Time (season + day)
                │     └─ Travel Tips
                │
                ├── Return Flight SubGraph
                │     ├─ Swap Origin/Destination
                │     ├─ Fetch Return Flights
                │     └─ Select Return Flight
                │
                └── Final Summary Node (LLM)
                    ├─ Consolidated Itinerary
                    ├─ Flights + Hotel + Weather
                    └─ Human-Readable Trip Plan


### Control Flow

                        START
                        ↓
                        User Input
                        ↓
                        Outbound Flight SubGraph
                        ↓
                        Decision Router (ask_next_step)
                        ├─→ Hotel SubGraph ──┐
                        ├─→ Weather SubGraph ─┤
                        ├─→ Travel LLM Node ──┤──→ back to Decision Router
                        └─→ Return Flight ────┘
                                ↓
                            Final Summary
                                ↓
                                END


