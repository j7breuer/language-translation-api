
# App Directory

### ```./restx_models```
This directory is where schemas are pulled from to enforce incoming requests.  ```./restx_models/schemas.py``` is where the schemas live and can be updated if any custom development is done after pulling repository.

---

### ```app.py```
This script initiates the API using the Flask framework and deploys all end points using the ```@api.route``` decorators.  

---

### ```helsinki_translation.py```
This script is the Python module imported in ```app.py``` to use the ```LanguageTranslation``` class.  This class has functions designed to:
- ```load_tokenizer```
  - Custom tokenizers can be utilized here, the current tokenizers used are from the ```Helsinki-NLP/opus-mt-{from_lang}-{to_lang}``` repository
- ```load_model```
  - Using the ```ct2-model-converter.sh``` script in the root directory, all models are stored in the models directory
- ```load_languages```
  - Leverages the two functions above and the languages in ```./models/lang_abbr_key.json``` to load all tokenizers and models
- ```sent_split```
  - Splits all sentences using the ```sent_tokenize``` function from ```nltk.tokenize```.  If a custom sentence splitting process is desired, the change should be implemented here. 
- ```translate_single```
  - Compiles request payload and translates
- ```translate_batch```
  - Loops through incoming array from payload and translates using the translate single function


