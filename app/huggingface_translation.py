
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LanguageTranslation:
    def __init__(self):
        self.gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model_prefix_name = "Helsinki-NLP/opus-mt-"
        self.languages_supported = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it"
        }
        self.models = defaultdict(dict)
    
    def load_tokenizer(self, from_lang: str, to_lang: str):
        '''
        desc: 
            Given two languages to translate from and to, return the Helsinki tokenizer.
            If tokenizer not already downloaded to disk, it will automatically download.
        inpt:
            from_lang [str]: 2 letter abbreviation of language to translate from.
            to_lang [str]: 2 letter abbreviation of language to translate to.
        oupt:
            [tokenizer]: AutoTokenizer object specific to language combination.
        '''
        # Create model string prefix for download/loading, uses helsinki model name
        model_string_name = f"{self.model_prefix_name}{from_lang}-{to_lang}"
        return AutoTokenizer.from_pretrained(model_string_name)

    def load_model(self, from_lang: str, to_lang: str):
        '''
        desc: 
            Given two languages to translate from and to, return the Helsinki model.
            If model not already downloaded to disk, it will automatically download.
        inpt:
            from_lang [str]: 2 letter abbreviation of language to translate from.
            to_lang [str]: 2 letter abbreviation of language to translate to.
        oupt:
            [model]: AutoModel object specific to language combination.
        '''
        # Create model string name for download/loading, uses helsinki model name
        model_string_name = f"{self.model_prefix_name}{from_lang}-{to_lang}"
        return AutoModelForSeq2SeqLM.from_pretrained(model_string_name).to(self.gpu)

    def load_languages(self):
        '''
        desc:
            Given list of languages to be able to translate, load the tokenizer/models
            into the self.models dict to be referenced downstream.
            Only supports translating to English currently.
        oupt:
            self.models [dict]: updated with tokenizer/model combos from lang_list.
        '''
        # Iterate through languages supported to initiate all models/tokenizers
        for k,v in self.languages_supported.items():
            # Skip english
            if k != "English":
                # Store in class so it can be referenced internally
                self.models[f"{v}-en"]["tokenizer"] = self.load_tokenizer(v, "en")
                self.models[f"{v}-en"]["model"] = self.load_model(v, "en")

    def translate_single(self, from_lang: str, to_lang: str, text: list) -> list:
        '''
        desc:
            Given a from_lang, to_lang, and text, translate the text using transformer models.
            Runs very slow on CPU, is configured to run on GPU.
        inpt:
            from_lang [str]: 2 letter abbreviation of langauge to translated from.
            to_lang [str]: 2 letter abbreviation of language to translate to.
            text [list]: list of strings to translate.
        '''
        # Tokenize the text using tokenizer stored in class
        tokenized_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"].prepare_seq2seq_batch(text, return_tensors = "pt").to(self.gpu)
        # Generate translated tokens using model stored in class
        translated_tokens = self.models[f"{from_lang}-{to_lang}"]["model"].generate(**tokenized_text)
        # Convert translated tokens to english text using tokenizer stored in class
        translated_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"].batch_decode(translated_tokens, skip_special_tokens = True)
        torch.cuda.empty_cache()
        return translated_text

    def deconstruct_inpt(self, inpt_list: list) -> list:
        '''
        desc:
            Given an inpt list of dicts, add a placement k,v pair starting from 0.
        inpt:
            inpt_list [list]: list of dicts to add the new placement k,v pair.
        oupt:
            [list]: list of dicts with new k,v pair.
        '''
        # Add placement key,value pair to dictionary
        return [dict(item, **{"placement": count}) for count, item in enumerate(inpt_list, 0)]

    def reconstruct_inpt(self, inpt_list: list) -> list:
        '''
        desc:
            Given an inpt list of dicts, sort the list on the placement key within each dict.
            This ensures that the API's response is in the same order it was received.
        inpt:
            inpt_list [list]: list of dicts that have a k,v pair for 'placement'.
        oupt:
            [list]: sorted list of dictionaries on the placement key.
        '''
        # Reorder based on placement key,value pair in dictionary
        return sorted(inpt_list, key = lambda k: k["placement"])

    def translate_batch(inpt_list: list):
        '''
        desc:
            Given a list of dictionaries with from_lang and text, translate in batch.
        inpt:
            inpt_list [list]: list of dicts that have the k,v pairs:
                - from_lang [str]: 2 letter abbreviation of language.
                - text [str]: text to be translated.
        oupt:
            oupt_list [list]: inpt_list where each dict has a new k,v pair of translated text.
        '''
        # Create a list of all foreign languages to translate from into english
        inpt_list = self.deconstruct_inpt(inpt_list)
        foreign_lang_list = list(set([x["from_lang"] for x in inpt_list]))
        # Loop through languages and translate in batches
        oupt_list = []
        for lang in foreign_lang_list:
            # Pull all dicts from certain langauge
            cur_lang_inpt_list = [x for x in inpt_list if x["from_lang"] == lang]
            # Translate text in batch
            translated_text = self.translate_single(lang, "en", [x["text"] for x in cur_lang_inpt_list])
            cur_lang_inpt_list = [dict(item, **{"translated_text": translated_text[count]}) for count, item in enumerate(translated_text, 0)]
            # Append list of dicts to oupt list
            oupt_list = oupt_list + cur_lang_inpt_list
        # Reorder the list of dicts
        oupt_list = self.reconstruct_inpt(oupt_list)
        return oupt_list
            


