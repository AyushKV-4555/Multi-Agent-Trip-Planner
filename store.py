# store.py

# Key format: "SOURCE_DESTINATION"
# Example: "Delhi_Mumbai"

FLIGHT_STORE = {
    "Delhi_Mumbai": [
        {
            "airline": "IndiGo",
            "flight_no": "6E-201",
            "totals": {"total": 5200},
            "duration": {"value": 130},
            "departure": "08:00",
            "arrival": "10:10"
        }
    ],

    "Mumbai_Delhi": [
        {
            "airline": "Vistara",
            "flight_no": "UK-945",
            "totals": {"total": 7500},
            "duration": {"value": 120},
            "departure": "07:00",
            "arrival": "09:00"
        }
    ],

    # 🌴 Goa routes
    "Delhi_Goa": [
        {
            "airline": "IndiGo",
            "flight_no": "6E-5231",
            "totals": {"total": 6800},
            "duration": {"value": 155},
            "departure": "06:10",
            "arrival": "08:45"
        }
    ],

    # 🌴 Goa routes
    "Goa_Delhi": [
        {
            "airline": "Akasa Air",
            "flight_no": "6E-5131",
            "totals": {"total": 9000},
            "duration": {"value": 145},
            "departure": "06:10",
            "arrival": "08:45"
        }
    ],

    # 🏙 Pune routes
    "Delhi_Pune": [
        {
            "airline": "Vistara",
            "flight_no": "UK-997",
            "totals": {"total": 6900},
            "duration": {"value": 140},
            "departure": "07:30",
            "arrival": "09:50"
        }
    ],

    # 🌆 Lucknow routes
    "Delhi_Lucknow": [
        {
            "airline": "IndiGo",
            "flight_no": "6E-2134",
            "totals": {"total": 3600},
            "duration": {"value": 75},
            "departure": "09:00",
            "arrival": "10:15"
        }
    ],

    # 🏙 Pune routes
    "Pune_Delhi": [
        {
            "airline": "Vistara",
            "flight_no": "UK-097",
            "totals": {"total": 6000},
            "duration": {"value": 140},
            "departure": "07:30",
            "arrival": "09:50"
        }
    ],

    # 🌆 Lucknow routes
    "Lucknow_Delhi": [
        {
            "airline": "IndiGo",
            "flight_no": "6E-3334",
            "totals": {"total": 3000},
            "duration": {"value": 75},
            "departure": "01:00",
            "arrival": "11:15"
        }
    ],

    "Mumbai_Lucknow": [
        {
            "airline": "Air India",
            "flight_no": "AI-626",
            "totals": {"total": 5900},
            "duration": {"value": 150},
            "departure": "11:20",
            "arrival": "13:50"
        }
    ],

    "Lucknow_Mumbai": [
        {
            "airline": "Air India",
            "flight_no": "AI-6726",
            "totals": {"total": 2000},
            "duration": {"value": 120},
            "departure": "12:20",
            "arrival": "13:50"
        }
    ]
}


HOTEL_STORE = {
    "Delhi": [
        {
            "name": "Taj Palace",
            "place": "Chanakyapuri",
            "url": "https://tajhotels.com/taj-palace-delhi"
        },
        {
            "name": "The Leela Ambience",
            "place": "East Delhi",
            "url": "https://theleela.com"
        }
    ],

    "Mumbai": [
        {
            "name": "Trident Nariman Point",
            "place": "Nariman Point",
            "url": "https://tridenthotels.com"
        },
        {
            "name": "ITC Maratha",
            "place": "Andheri East",
            "url": "https://itchotels.com"
        }
    ],

    "Goa": [
        {
            "name": "Taj Fort Aguada",
            "place": "Candolim",
            "url": "https://tajhotels.com"
        },
        {
            "name": "Leela Goa",
            "place": "Mobor Beach",
            "url": "https://theleela.com"
        }
    ],

    "Pune": [
        {
            "name": "JW Marriott Pune",
            "place": "Senapati Bapat Road",
            "url": "https://marriott.com"
        },
        {
            "name": "Hyatt Regency",
            "place": "Viman Nagar",
            "url": "https://hyatt.com"
        }
    ],

    "Lucknow": [
        {
            "name": "Taj Mahal Lucknow",
            "place": "Gomti Nagar",
            "url": "https://tajhotels.com"
        },
        {
            "name": "Hyatt Regency",
            "place": "Vibhuti Khand",
            "url": "https://hyatt.com"
        }
    ]
}
