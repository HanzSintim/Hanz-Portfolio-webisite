"""Portfolio project data. Imported by app.py and rendered in the templates."""

# Each project is one dictionary. All the pages and the JSON API read from this list.
# slug       = short URL-friendly name for the project
# category   = must be exactly "Embedded & Hardware" or "Software & Systems"
#              (the filter links on the Projects page match against this text)
# tech_stack = list of tools/languages (shown as badges)
# highlights = 2-3 technical bullet points
PROJECTS = [
    {
        "slug": "street-cleaning-robot",
        "title": "Autonomous Street-Cleaning Robot Prototype",
        "category": "Embedded & Hardware",
        "tech_stack": ["C/C++", "Sensor Modules", "Motor Control"],
        "summary": (
            "A prototype robot that moves on its own and detects obstacles "
            "while cleaning a street surface."
        ),
        "highlights": [
            "Read distance sensor modules to detect and avoid obstacles.",
            "Wrote C/C++ firmware to drive the motors and control movement.",
            "Combined sensing and actuation into one autonomous control loop.",
        ],
    },
    {
        "slug": "custom-power-charger-pcb",
        "title": "Custom Power Charger PCB",
        "category": "Embedded & Hardware",
        "tech_stack": [
            "KiCad",
            "Schematic Capture",
            "Chemical Copper Etching",
            "Linear Regulation",
        ],
        "summary": (
            "A charger board designed in KiCad and built by hand, "
            "from schematic to etched copper."
        ),
        "highlights": [
            "Captured the schematic and laid out the PCB in KiCad.",
            "Fabricated the board by chemical copper etching.",
            "Used linear regulation to give a stable charging voltage.",
        ],
    },
    {
        "slug": "water-tank-monitoring",
        "title": "Automatic Water Tank Monitoring & Control System",
        "category": "Embedded & Hardware",
        "tech_stack": [
            "Arduino",
            "Ultrasonic Sensors",
            "LCD Interface",
            "Closed-Loop Control",
        ],
        "summary": (
            "An Arduino system that measures the water level and "
            "controls the pump automatically."
        ),
        "highlights": [
            "Measured water level with an ultrasonic sensor.",
            "Showed the live level on an LCD display.",
            "Closed-loop control switches the pump on and off by itself.",
        ],
    },
    {
        "slug": "shopping-mall-management",
        "title": "Shopping Mall Management System",
        "category": "Software & Systems",
        "tech_stack": ["C++", "OOP", "Data Structures", "Team Lead"],
        "summary": (
            "A C++ application that manages the shops, items and records "
            "of a shopping mall."
        ),
        "highlights": [
            "Modelled the mall with object-oriented classes.",
            "Chose suitable data structures to store and search records.",
            "Led the team: split tasks and integrated everyone's code.",
        ],
    },
    {
        "slug": "logistics-delivery-database",
        "title": "Smart Logistics & Delivery Management Database",
        "category": "Software & Systems",
        "tech_stack": ["SQL", "ER Diagramming", "Relational Schema Normalization"],
        "summary": (
            "A relational database designed to track orders, drivers "
            "and deliveries."
        ),
        "highlights": [
            "Drew the ER diagram to map entities and relationships.",
            "Normalized the relational schema to remove redundant data.",
            "Wrote SQL to create tables and query delivery information.",
        ],
    },
]
