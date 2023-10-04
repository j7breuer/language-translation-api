#!/bin/bash

# Loop through keys in the JSON and download the models and convert, storing in ./app/models
jq -r 'keys[]' "$1" | while read -r key; do
  # If key is 'en' then skip
  if [ "${key}" == "en" ]; then
    continue
  fi

  # Convert models
  ct2-transformers-converter --model Helsinki-NLP/opus-mt-${key}-en --output_dir ./app/models/${key}_en --force

done