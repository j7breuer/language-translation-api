

import json
from flask import Flask, jsonify, abort
from flask_restx import Resource, Api, fields
from requests.api import request
from restx_models.schemas import api as translation_models
from flask_restx.apidoc import apidoc
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_translation import LanguageTranslation
import torch
import sys

# Initiate all models/tokenizers for translation
lt = LanguageTranslation()
lt.load_languages()

# Load api
app = Flask(__name__)
api = Api(app)

api.add_namespace(translation_models)

@api.route("/help", methods = ["GET"])
class help(Resource):
    def get(self):
        return {
            "message": "This is an API meant to conduct basic translations between various languages using various transformer based language translation models."
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
            "message": "Languages supported: English, Spanish, French, German, Italian."
        }

@api.route("/translation/single", methods = ["POST"])
class translation_single(Resource):
    @api.expect(translation_models.models["translation_single"], validate = True)
    def post(self):
        data = api.payload
        # Do something
        from_lang = data["from_lang"]
        to_lang = data["to_lang"]
        text = data["text"]

        oupt = lt.translate_single(from_lang, to_lang, [text])

        return jsonify(
            {
                "message": f"Message translated from {from_lang} to English.",
                "data": {
                    "request": {
                        "from_lang": from_lang,
                        "to_lang": to_lang,
                        "model_name": f"{lt.model_prefix_name}{from_lang}-{to_lang}"
                    },
                    "response": oupt[0]
                }
            }
        )

@api.route("/translation/batch", methods = ["POST"])
class translation_batch(Resource):
    @api.expect(translation_models.models["translation_batch"], validate = True)
    def post(self):
        data = api.payload
        oupt = lt.translate_batch(data)
        return jsonify(
            {
                "message": f"Batch results of {len(oupt)} messages",
                "data": {
                    "response": oupt
                }
            }
        )

if __name__ == "__main__":
    app.run(debug = True)