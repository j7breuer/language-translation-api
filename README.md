
# Language Tranlsation Microservice [Test]
API that provides language translation capabilities using the latest HuggingFace Helsinki models.  This API takes in text from 5 languages currently and can translate accordingly.


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