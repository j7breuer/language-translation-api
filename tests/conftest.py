

import pytest
import sys
import json

sys.path.append("./app")
with open('./models/lang_abbr_key.json') as f:
    abbr_key = json.load(f)

from app import app as root_app

@pytest.fixture(scope = "session")
def client():
    root_app.testing = True
    with root_app.test_client() as client:
        yield client

@pytest.fixture()
def get_help():
    oupt = {
        "message": "This is an API meant to conduct basic translations between 4 languages and English using various transformer based language translation models."
    }
    return oupt

@pytest.fixture()
def get_help_single():
    oupt = {
        "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
    }
    return oupt

@pytest.fixture()
def get_help_batch():
    oupt = {
        "message": "Using models from the HuggingFace community, translate text in batch between two languages via this API call."
    }
    return oupt

@pytest.fixture()
def get_help_languages():
    oupt = {
        "message": "Languages supported: English, Spanish, German."
    }
    return oupt

@pytest.fixture()
def expected_translation_single():
    oupt = {}
    from_lang = 'en'
    to_lang = 'es'
    text = 'Hi, how are you doing?'
    oupt['request'] = {
        "from_lang": from_lang,
        "to_lang": to_lang,
        "text": text
    }
    oupt['response'] = {
        "message": f"Message translated from {abbr_key[from_lang]} to {abbr_key[to_lang]}.",
        "data": {
            "request": {
                "from_lang": from_lang,
                "to_lang": to_lang,
                "model_name": f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}"
            },
            "response": {
                "text": "Hola, ¿cómo estás?"
            }
        }
    }
    return oupt

@pytest.fixture()
def expected_translation_batch():
    oupt = {}
    from_lang = 'en'
    to_lang = 'es'
    text = [
        "Hi, how are you doing?",
        "I'm doing good and you?",
        "Pretty good, just looking forwards to finishing unit tests..."
    ]
    oupt['request'] = {
        "from_lang": from_lang,
        "to_lang": to_lang,
        "text": text
    }
    oupt['response'] = {
        "message": f"Message translated from {abbr_key[from_lang]} to {abbr_key[to_lang]}.",
        "data": {
            "request": {
                "from_lang": from_lang,
                "to_lang": to_lang,
                "model_name": f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}"
            },
            "response": {
                "text": [
                    "Hola, ¿cómo estás?",
                    "¿Lo estoy haciendo bien y tú?",
                    "Bastante bien, sólo con ganas de terminar las pruebas de unidad..."
                ]
            }
        }
    }
    return oupt
