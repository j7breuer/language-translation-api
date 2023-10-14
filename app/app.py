

import json
import os
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api, fields
from requests.api import request
from restx_models.schemas import api as translation_models
from flask_restx.apidoc import apidoc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from helsinki_translation import LanguageTranslation
import torch
import sys

# Initiate all models/tokenizers for translation
lt = LanguageTranslation()

# Define languages supported
with open("./models/lang_abbr_key.json") as f:
    abbr_key = json.load(f)
lt.languages_supported = abbr_key

# Set master language, already set as default
# lt.master_lang = "en"

# Set cpu device
lt.device = "cpu"

# Set direction of translations (unidirectional vs. bidirectional), already set as default
# lt.direction = "bidirectional"

# Load all tokenizers/models
lt.load_languages()

# Load api and add namespace for schemas
app = Flask(__name__)
api = Api(app)
api.add_namespace(translation_models)

@api.route("/help", methods = ["GET"])
class help(Resource):
    def get(self):
        return {
            "message": "This is an API meant to conduct basic translations between 2 languages and English using various transformer based language translation models."
        }

@api.route("/help/single", methods = ["GET"])
class help_single(Resource):
    def get(self):
        return {
            "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
        }

@api.route("/help/batch", methods = ["GET"])
class help_batch(Resource):
    def get(self):
        return {
            "message": "Using models from the HuggingFace community, translate text in batch between two languages via this API call."
        }

@api.route("/help/languages", methods = ["GET"])
class help_languages(Resource):
    def get(self):
        return {
            "message": f"Languages supported: {', '.join(abbr_key.values())}."
        }

@api.route("/translation/single", methods = ["POST"])
class translation_single(Resource):
    @api.expect(translation_models.models["translation_single"], validate = True)
    def post(self):
        data = api.payload
        # Extract request vars
        from_lang = data["from_lang"]
        to_lang = data["to_lang"]
        text = data["text"]
        # Translate single
        oupt = lt.translate_single(from_lang, to_lang, text)

        return jsonify(
            {
                "message": f"Message translated from {abbr_key[from_lang]} to {abbr_key[to_lang]}.",
                "data": {
                    "request": {
                        "from_lang": from_lang,
                        "to_lang": to_lang
                    },
                    "response": {
                        "text": oupt,
                        "model": f"{lt.model_prefix_name}{from_lang}-{to_lang}",
                        "tokenizer": f"{lt.model_prefix_name}{from_lang}-{to_lang}",
                        "device": f"{lt.device}"
                    }
                }
            }
        )

@api.route("/translation/batch", methods = ["POST"])
class translation_batch(Resource):
    @api.expect(translation_models.models["translation_batch"], validate = True)
    def post(self):
        data = api.payload
        # Extract request vars
        from_lang = data["from_lang"]
        to_lang = data["to_lang"]
        text = data['text']
        # Translate in batch
        oupt = lt.translate_batch(from_lang, to_lang, text)

        return jsonify(
            {
                "message": f"Batch results of {len(oupt)} messages translated from {abbr_key[from_lang]} to {abbr_key[to_lang]}.",
                "data": {
                    "request": {
                        "from_lang": from_lang,
                        "to_lang": to_lang
                    },
                    "response": {
                        "text": oupt,
                        "model": f"{lt.model_prefix_name}{from_lang}-{to_lang}",
                        "tokenizer": f"{lt.model_prefix_name}{from_lang}-{to_lang}",
                        "device": f"{lt.device}"
                    }
                }
            }
        )

# Run app, bind to local ip and port 4567
if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = False, port = 4567)