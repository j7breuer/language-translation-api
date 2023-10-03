#!/bin/bash

# Loop through keys in the JSON and download the models and convert, storing in ./app/models
jq -r 'keys[]' "$1" | while read -r key; do
  ct2-transformers-converter --model Helsinki-NLP-opus-mt-$key-en --output_dir ./app/models/$key_en
done