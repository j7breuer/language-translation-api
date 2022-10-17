#!/bin/bash
curl -i -H "Content-Type: application/json" -X POST -d "{\"from_lang\": \"es\", \"to_lang\":\"en\", \"text\": \"hola como estas?\"}" http://127.0.0.1:5000/translation/single