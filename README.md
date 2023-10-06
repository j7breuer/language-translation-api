
# Language Tranlsation Microservice [Beta]
Flask-based API that provides language translation capabilities using the latest <a href="https://marian-nmt.github.io/">MarianNMT</a> models developed by the <a href="https://blogs.helsinki.fi/language-technology/">Language Technology Research Group at the University of Helsinki</a>.  All model inference times are enhanced using <a href="https://github.com/OpenNMT/CTranslate2">CTranslate2</a>, a C++ and Python library built to optimize transformer models.  This API is fully customizable, by default it takes in text from 3 languages currently and can translate bi-directionally with English (to, from).  The API comes with a single and batch endpoint for translations.

The <a href="https://blogs.helsinki.fi/language-technology/">Language Technology Research Group at the University of Helsinki's</a> models built on the <a href="https://marian-nmt.github.io/">MarianNMT</a> framework benefit from:
- CPU or GPU translation
- Efficient pure C++ implementation if desired
- Over 1,400 translation models between 100+ languages
  - Check out the <a href="https://huggingface.co/Helsinki-NLP?sort_models=downloads#models">HuggingFace page</a> to search models
- Active developer community 

## Customization
### Adding, Removing, Updating Languages [Optional]
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

### Changing Master Language [Optional]
#### <u>[Default] Master Language</u>: English
The API is configured to set English as the 'master' language.  The 'master' language determines the direction of translations between languages in the ```./models/lang_abbr_key.json``` file.  By default, all translations are bi-directional between the 'master' language and other languages in the ```./models/lang_abbr_key.json``` file.

To change the default master language, update the ```./app/app.py``` file below to the new language abbreviation.
```
L23: # Set master language, already set as default
L24: lt.master_lang = "es"
```

### Changing Direction [Optional]
#### <u>[Default] Direction</u>: Bidirectional
The API can be updated from bidirectionally to unidirectionally to translate between languages.  

To change the default direction, update the ```./app/app.py``` file below to the new config:
```
L26: # Set direction of translations, bidirectional by default
L27: lt.direction = "unidirectional"

```

### CPU or GPU Translations [Optional]
#### <u>[Current] Configuration</u>: CPU only, <i>GPU integration still in development</i>
The API will be able to detect the presence of a GPU on the system, if a GPU is available, all translations will be routed to GPU instead of CPU.  If GPU is not detected, all translations will be sent to CPU.

Space and build time can be saved if you intend to use CPU only by commenting out line 24 of the Dockerfile and uncommenting line 22 to remove the installation of CUDA.  

### CI / CD Integration [Optional]
The repository does not need to be integrated with CI / CD services but can be easily configured to integrate with Sonarqube, Jenkins, and other services such as Nexus, MLFlow, and more.

If integrating with CI / CD services, please update associated files below:
- ```./Jenkinsfile``` for Jenkins orchestration
- ```./sonar-project.properties``` for Sonarqube scans
- ```./pip.conf``` and ```./Dockerfile``` for referencing custom PyPi

#### Current Metrics:
1. Code Coverage: XX.XX%
2. Code Smells: 
3. Vulnerabilities:

# Deploying
## Docker Deployment
### Docker Build
```
docker build -t language_translation_api
```

### Docker Run
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
            "model_name": "Helsinki-NLP/opus-mt-es-en",
            "to_lang": "en"
        },
        "response": "Hello how are you?"
    },
    "message": "Message translated from es to English."
}
```

## Endpoints:

### GET API Help

'GET /help'

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
}
```

### GET API Help Single

'GET /help/single'

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text via single calls between two languages via this API endpoint."
}
```

### GET API Help Batch

'GET /help/batch'

**Response**

- '200 OK' on success

```json
{
    "message": "Using models from the HuggingFace community, translate text in batch between two languages via this API call."
}
```

### POST Translation Single

'POST /translation/single'

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
      "model_name": "Helsinki-NLP/opus-mt-es-en",
      "to_lang": "en"
    },
    "response": "Hello how are you?"
  },
  "message": "Message translated from es to English."
}
```
