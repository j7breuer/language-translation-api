
# Language Tranlsation Microservice [Beta]
API that provides language translation capabilities using the latest HuggingFace Helsinki models.  This API takes in text from 4 languages currently and can translate into English only.   


## Installation
By default, the language translation models will run off of CPU.  If you'd like to run off of GPU to speed up duration of translations, please configure torch to point to your GPU.

### Install requirements.txt first
```
pip install -r requirements.txt
```

### You may need to install sentencepiece an alternative way
```
pip install transformers[sentencepiece]
```

### Install PyTorch and CUDA accordingly
You can do this by defaulting to the specifications of requirements.txt or by going to the following website and using the onscreen prompt: https://pytorch.org/get-started/locally/


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
