#!/bin/bash

# Loop through keys in the JSON and download the models and convert, storing in ./app/models
jq -r 'keys[]' "$1" | while read -r key; do
  # If key is 'en' then skip
  if [ "${key}" == "en" ]; then
    continue
  fi

  # Convert models from english to language
  echo "Downloading and converting: ${key}-en..."
  ct2-transformers-converter --model Helsinki-NLP/opus-mt-${key}-en --output_dir ./models/${key}_en

  # Convert models from language to english
  echo "Downloading and converting: en-${key}..."
  ct2-transformers-converter --model Helsinki-NLP/opus-mt-en-${key} --output_dir ./models/en_${key}

done