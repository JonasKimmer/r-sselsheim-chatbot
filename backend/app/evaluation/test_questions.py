"""Test dataset for evaluating the Rüsselsheim chatbot."""

from typing import List, Dict

# Test questions covering different categories
TEST_QUESTIONS: List[Dict[str, str]] = [
    # Verwaltung / Administration
    {
        "question": "Wie beantrage ich einen Personalausweis?",
        "category": "verwaltung",
        "description": "Basic administrative question about ID cards"
    },
    {
        "question": "Welche Dokumente brauche ich für einen Reisepass?",
        "category": "verwaltung",
        "description": "Passport application requirements"
    },
    {
        "question": "Wo ist das Bürgerbüro und wann hat es geöffnet?",
        "category": "verwaltung",
        "description": "Citizen office location and hours"
    },
    {
        "question": "Wie melde ich meinen Wohnsitz um?",
        "category": "verwaltung",
        "description": "Residence registration"
    },
    {
        "question": "Kann ich einen Termin im Bürgerbüro online buchen?",
        "category": "verwaltung",
        "description": "Online appointment booking"
    },

    # Wetter / Weather
    {
        "question": "Wie wird das Wetter morgen in Rüsselsheim?",
        "category": "wetter",
        "description": "Weather forecast"
    },
    {
        "question": "Regnet es heute?",
        "category": "wetter",
        "description": "Current weather conditions"
    },
    {
        "question": "Wie kalt ist es gerade?",
        "category": "wetter",
        "description": "Current temperature"
    },

    # Verkehr / Traffic & Transit
    {
        "question": "Wie komme ich vom Hauptbahnhof zum Rathaus?",
        "category": "verkehr",
        "description": "Public transit directions"
    },
    {
        "question": "Wann fährt die nächste Bahn nach Frankfurt?",
        "category": "verkehr",
        "description": "Train schedule"
    },
    {
        "question": "Gibt es Stau auf der A67?",
        "category": "verkehr",
        "description": "Traffic conditions"
    },

    # Abfall / Waste Management
    {
        "question": "Wann wird bei mir der Müll abgeholt?",
        "category": "abfall",
        "description": "Waste collection schedule"
    },
    {
        "question": "Wo kann ich Sperrmüll entsorgen?",
        "category": "abfall",
        "description": "Bulky waste disposal"
    },
    {
        "question": "Wann kommt die Biotonne?",
        "category": "abfall",
        "description": "Organic waste collection"
    },

    # Benzinpreise / Fuel Prices
    {
        "question": "Wo gibt es das günstigste Benzin in Rüsselsheim?",
        "category": "benzin",
        "description": "Cheapest fuel prices"
    },

    # Feiertage / Holidays
    {
        "question": "Wann ist der nächste Feiertag in Hessen?",
        "category": "feiertage",
        "description": "Next public holiday"
    },
    {
        "question": "Ist morgen ein Feiertag?",
        "category": "feiertage",
        "description": "Holiday check"
    },

    # Allgemeine Informationen / General Information
    {
        "question": "Wie viele Einwohner hat Rüsselsheim?",
        "category": "allgemein",
        "description": "City statistics"
    },
    {
        "question": "Was kann ich in Rüsselsheim unternehmen?",
        "category": "freizeit",
        "description": "Leisure activities"
    },
    {
        "question": "Welche Sehenswürdigkeiten gibt es in Rüsselsheim?",
        "category": "tourismus",
        "description": "Tourist attractions"
    },

    # Complex multi-domain questions
    {
        "question": "Ich möchte nächste Woche einen Personalausweis beantragen. Wie ist das Wetter und wie komme ich zum Bürgerbüro?",
        "category": "verwaltung",
        "description": "Multi-domain question combining administration, weather, and transit"
    }
]


def get_questions_by_category(category: str) -> List[Dict[str, str]]:
    """Get all test questions for a specific category."""
    return [q for q in TEST_QUESTIONS if q["category"] == category]


def get_all_questions() -> List[str]:
    """Get just the question strings."""
    return [q["question"] for q in TEST_QUESTIONS]


def get_all_test_cases() -> List[Dict[str, str]]:
    """Get all test cases with metadata."""
    return TEST_QUESTIONS


# Expected responses for validation (optional - for advanced evaluation)
EXPECTED_RESPONSES = {
    "Wie beantrage ich einen Personalausweis?": {
        "should_contain": [
            "biometrisches Passfoto",
            "Bürgerbüro",
            "Rathaus"
        ],
        "should_mention_category": "verwaltung"
    },
    "Wie wird das Wetter morgen in Rüsselsheim?": {
        "should_contain": [
            "Temperatur",
            "Grad"
        ],
        "should_use_api": "wetter"
    },
    "Wann fährt die nächste Bahn nach Frankfurt?": {
        "should_contain": [
            "Uhr",
            "Hauptbahnhof"
        ],
        "should_use_api": "rmv"
    }
}
