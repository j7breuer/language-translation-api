
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LanguageTranslation:
    def __init__(self):
        self.gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        #self.gpu = torch.device("cpu")
        self.model_prefix_name = "Helsinki-NLP/opus-mt-"
        self.languages_supported = {}
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
            if v != "English":
                # Store in class so it can be referenced internally
                self.models[f"{k}-en"]["tokenizer"] = self.load_tokenizer(k, "en")
                self.models[f"{k}-en"]["model"] = self.load_model(k, "en")
                self.models[f"en-{k}"]["tokenizer"] = self.load_tokenizer("en", k)
                self.models[f"en-{k}"]["model"] = self.load_model("en", k)
    
    def split_array(self, inpt_array: list, size_count: int) -> list:
        '''
        desc:
            Given a list, split it into sub lists with a specific size count
        inpt:
            inpt_array [list]: list to break into chunks
            size_count [int]: int of length to break sublists into
        oupt:
            [list[list]]: list of lists with sub lists
        '''
        return [inpt_array[i:i+size_count] for i in range(0,len(inpt_array), size_count)]


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
        tokenized_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"](text, return_tensors = "pt").to(self.gpu)
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

    def translate_batch(self, from_lang: str, to_lang: str, inpt_list: list):
        '''
        desc:
            Given a list of text, translate in batch.
        inpt:
            inpt_list [list]: list of strings in one language:
            from_lang [str]: 2-3 letter abbreviation of language.
            to_lang [str]: 2-3 letter abbreviation of language.
        oupt:
            oupt_list [list]: list of text translated into target language
        '''
        # Tokenize the text using tokenizer stored in class
        tokenized_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"](inpt_list, return_tensors = "pt", padding = True).to(self.gpu)
        torch.cuda.empty_cache()
        # Generate translated tokens using model stored in class
        translated_tokens = self.models[f"{from_lang}-{to_lang}"]["model"].generate(**tokenized_text)
        torch.cuda.empty_cache()
        # Convert translated tokens to english text using tokenizer stored in class
        translated_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"].batch_decode(translated_tokens, skip_special_tokens = True)
        torch.cuda.empty_cache()
        return translated_text
    
    def translate_batch_dicts(self, inpt_list: list):
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
        foreign_lang_list = list(set([x["from_lang"] for x in inpt_list if x != "en"]))
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
            


