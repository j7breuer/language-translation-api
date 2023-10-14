
# Language Translation Microservice [Beta] 
Flask-based API that provides language translation capabilities using the latest <a href="https://marian-nmt.github.io/">MarianNMT</a> models developed by the <a href="https://blogs.helsinki.fi/language-technology/">Language Technology Research Group at the University of Helsinki</a>.  All model inference times are enhanced using <a href="https://github.com/OpenNMT/CTranslate2">CTranslate2</a>, a C++ and Python library built to optimize transformer models.  This API is fully customizable, by default it takes in text from 3 languages currently and can translate bi-directionally with English (to, from).  The API comes with a single and batch endpoint for translations.

The <a href="https://blogs.helsinki.fi/language-technology/">Language Technology Research Group at the University of Helsinki's</a> models built on the <a href="https://marian-nmt.github.io/">MarianNMT</a> framework benefit from:
- CPU or GPU translation
- Efficient pure C++ implementation if desired
- Over 1,400 translation models between 100+ languages
  - Check out the <a href="https://huggingface.co/Helsinki-NLP?sort_models=downloads#models">HuggingFace page</a> to search models
- Active developer community 

## Customization
### <u>Adding, Removing, Updating Languages</u> [Optional]
#### <u>[Default] Languages</u>: English, Spanish, German
All languages included in the API are located in the ```./models/lang_abbr_key.json``` file as key-value pairs.
1. Search for translation model on <a href="https://huggingface.co/Helsinki-NLP?sort_models=downloads#models">HuggingFace page</a>
2. Edit the ```./models/lang_abbr_key.json``` file to contain languages in model 
3. Remove, add, or update key-value pairs
   1. Keys: 2 or 3 letter abbreviation of languages
   2. Values: Full name of language paired with key
4. Save ```./models/lang_abbr_key.json``` file
5. Build/rebuild your container

#### Warning: Container Size & Resources Needed
Please be mindful of the relationship between language (model) count and container size and hardware backing required to efficiently run.  The more models included, the more memory needed.  

<u>Example</u>: 
- Populating ```./models/lang_abbr_key.json``` with 10 languages will significantly increase container size, build time, and inference time depending on hardware backing the container deployment.
- 10 languages will mean a total of 20 tokenizers and 20 models

Consider deploying multiple containers with subsets of languages if desired.

---

### <u>Changing Master Language</u> [Optional]
#### <u>[Default] Master Language</u>: English
The API is configured to set English as the 'master' language.  The 'master' language determines the direction of translations between languages in the ```./models/lang_abbr_key.json``` file.  By default, all translations are bidirectional between the 'master' language and other languages in the ```./models/lang_abbr_key.json``` file.

To change the default master language, update the ```./app/app.py``` file below to the new language abbreviation.
```
L23: # Set master language, already set as default
L24: lt.master_lang = "es"
```

---

### <u>Changing Direction</u> [Optional]
#### <u>[Default] Direction</u>: Bidirectional
The API can be updated from bidirectional to unidirectional to translate between languages.  

To change the default direction, update the ```./app/app.py``` file below to the new config:
```
L26: # Set direction of translations, bidirectional by default
L27: lt.direction = "unidirectional"
```

---

### <u>CPU or GPU Translations</u> [Optional]
#### <u>[Current] Configuration</u>: GPU if present, CPU if not</i>
Using CTranslate2's device argument of ```auto```, the API will default to GPU if present and use CPU if GPU isn't detected.  To manually override the ```auto``` configuration, set ```lt.device = "cpu"``` or ```lt.device = "cuda"``` in app.py. 

For CPU-only implementation, please use the ```cpu-only``` branch.

If deploying with the intention of using GPU, ensure Docker is configured to connect to GPU - Windows 11 is configured to access GPUs via Docker containers.  If running Windows 10 and below, additional steps will need to be taken to enable Docker to connect to GPU.  By default, the ```master``` branch is set up to be configured for GPU but will fall back to CPU if no GPU is detected.  

#### Troubleshooting
If a GPU is present and errors occur when hitting the translation endpoints, it is most likely related to Docker not being able to connect to GPU.

1. Check to make sure Nvidia drivers are up-to-date
2. Check for potential version incompatibility between GPU and docker build
3. If on Windows 10, additional steps will need to be taken to enable GPU connection on Docker
---

### <u>CI / CD Integration</u> [Optional]
The repository does not need to be integrated with CI / CD services but can be easily configured to integrate with Sonarqube, Jenkins, and other services such as Nexus, MLFlow, and more.

If integrating with CI / CD services, please update associated files below:
- ```./Jenkinsfile``` for Jenkins orchestration
- ```./sonar-project.properties``` for Sonarqube scans
- ```./pip.conf``` and ```./Dockerfile``` for referencing custom PyPi

#### Current Metrics:
1. Code Coverage: 93.9%
2. Code Smells: 7
3. Vulnerabilities: 0

---
# Deploying
There are two options for deployment, via Docker or locally in terminal.  Instructions for both are below:
## Clone Repository
```
git clone https://github.com/j7breuer/language-translation-api.git
```
## Docker Deployment
### Docker Build
```
docker build -t language_translation_api
```

### [GPU] Docker Run
```
docker run --gpus all -d --name language-translation-api --restart=unless-stopped -p 4567:4567 language_translation_api 
```

### [CPU] Docker Run
```
docker run -d --name language-translation-api --restart=unless-stopped -p 4567:4567 language_translation_api 
```

## Local Deployment
### Installation of requirements
```
pip -r requirements.txt
python -m nltk.downloader punkt

# Optional if GPU used - please update depending on OS
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
```

### Install and convert CTranslate2 models
Change < from > and < to > to the language abbreviations of model to download and install into output directory. 
```
ct2-transformers-converter --model Helsinki-NLP/opus-mt-<from>-<to> --output_dir ./models/<from>_<to> --force
```

### Run Flask API locally 
```
python ./app/app.py
```

## Usage

Expect response to follow this format:

```json
{
    "data": {
        "request": {
            "from_lang": "es",
            "to_lang": "en"
        },
        "response": {
          "text": "Hello how are you?",
          "model": "Helsinki-NLP/opus-mt-es-en",
          "tokenizer": "Helsinki-NLP/opus-mt-es-en",
          "device": "auto",
        }
    },
    "message": "Message translated from Spanish to English."
}
```

## Endpoints:

### GET API Help

```GET /help```

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
}
```

### GET API Help Single

```GET /help/single```

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
}
```

### GET API Help Batch

```GET /help/batch```

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text in batch between two languages via this API call."
}
```

### POST Translation Single

```/translation/single```

**Request**
```json
{
    "from_lang": "es",
    "to_lang": "en",
    "text": "Hola como estas?"
}
```

**Response**
- '200 OK' on success

```json
{
  "data": {
    "request": {
      "from_lang": "es",
      "to_lang": "en"
    },
    "response": {
      "text": "Hello how are you?",
      "model": "Helsinki-NLP/opus-mt-es-en",
      "tokenizer": "Helsinki-NLP/opus-mt-es-en",
      "device": "auto"
    }
  },
  "message": "Message translated from Spanish to English."
}
```

### POST Translation Batch

```POST /translation/single```

**Request**
```json
{
    "from_lang": "es",
    "to_lang": "en",
    "text": [
      "Hola como estas?",
      "Bien y tu?"
    ]
}
```

**Response**
- '200 OK' on success

```json
{
  "data": {
    "request": {
      "from_lang": "es",
      "to_lang": "en"
    },
    "response": {
      "text": [
        "Hello how are you?",
        "Good and you?"
      ],
      "model": "Helsinki-NLP/opus-mt-es-en",
      "tokenizer": "Helsinki-NLP/opus-mt-es-en",
      "device": "auto"
    }
  },
  "message": "Batch results of 2 messages translated from Spanish to English."
}
```
