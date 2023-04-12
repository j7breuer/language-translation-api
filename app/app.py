

import json
import os
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
# Define language dict
with open("./app/lang_abbr_key.json") as f:
    abbr_key = json.load(f)
lt.languages_supported = abbr_key
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
sys.stdout.write("PyTorch Env. Var Set\n")

lt.load_languages()

# Load api
app = Flask(__name__)
api = Api(app)

api.add_namespace(translation_models)

@api.route("/help", methods = ["GET"])
class help(Resource):
    def get(self):
        return {
            "message": "This is an API meant to conduct basic translations between 4 languages and English using various transformer based language translation models."
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
                "message": f"Message translated from {from_lang} to {to_lang}.",
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
        from_lang = data["from_lang"]
        to_lang = data["to_lang"]
        oupt_array = []
        for sub_batch in lt.split_array(data['text'], 50):
            oupt = lt.translate_batch(from_lang, to_lang, sub_batch)
            oupt_array.extend(oupt)

        return jsonify(
            {
                "message": f"Batch results of {len(oupt_array)} messages translted from {from_lang} to {to_lang}.",
                "data": {
                    "request": {
                        "from_lang": from_lang,
                        "to_lang": to_lang,
                        "model_name": f"{lt.model_prefix_name}{from_lang}-{to_lang}"
                    },
                    "response": oupt_array
                }
            }
        )

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = False, port = 4567)