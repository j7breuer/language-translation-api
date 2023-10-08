
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import ctranslate2
from tqdm import tqdm

class LanguageTranslation:
    def __init__(self):
        self.device = "auto" # defaults to gpu if present, cpu if not - other argument options: cuda, cpu
        self.master_lang = "en"
        self.direction = "bidirectional"
        self.model_prefix_name = "Helsinki-NLP/opus-mt-"
        self.model_dir = "./models"
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
        model_string_name = f"{self.model_dir}/{from_lang}_{to_lang}"
        model = ctranslate2.Translator(model_string_name, device = self.device)
        return model

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
            if k != self.master_lang:
                # Store in class so it can be referenced internally
                if self.direction == "bidirectional":
                    self.models[f"{k}-{self.master_lang}"]["tokenizer"] = self.load_tokenizer(k, self.master_lang)
                    self.models[f"{k}-{self.master_lang}"]["model"] = self.load_model(k, self.master_lang)
                    self.models[f"{self.master_lang}-{k}"]["tokenizer"] = self.load_tokenizer(self.master_lang, k)
                    self.models[f"{self.master_lang}-{k}"]["model"] = self.load_model(self.master_lang, k)
                elif self.direction == "unidirectional":
                    self.models[f"{k}-{self.master_lang}"]["tokenizer"] = self.load_tokenizer(k, self.master_lang)
                    self.models[f"{k}-{self.master_lang}"]["model"] = self.load_model(k, self.master_lang)
                else:
                    pass
    def nltk_sent_split(self, text: str) -> list:
        '''
        desc:
            Given text from any language, use NLTK's sentence splitter to split into sentences
            for further processing
        inpt:
            text [str]: text to be split by sentences, language does not matter
        oupt:
            [list]: list of sentences
        '''
        return sent_tokenize(text)

    def translate_single(self, from_lang: str, to_lang: str, text: str) -> list:
        '''
        desc:
            Given a from_lang, to_lang, and text, translate the text using transformer models.
            Runs very slow on CPU, is configured to run on GPU.
        inpt:
            from_lang [str]: 2 letter abbreviation of langauge to translated from.
            to_lang [str]: 2 letter abbreviation of language to translate to.
            text [str]: string to translate.
        oupt:
            oupt_text [str]: string of translated text
        '''
        # Split by sentence
        split_sent = self.nltk_sent_split(text)
        # Create array to append to
        ts = []
        # Tokenize split sentences and append encoded oupt for model
        [ts.append(self.models[f"{from_lang}-{to_lang}"]["tokenizer"].convert_ids_to_tokens(self.models[f"{from_lang}-{to_lang}"]["tokenizer"].encode(i))) for i in split_sent]
        # Translate from model
        results = self.models[f"{from_lang}-{to_lang}"]["model"].translate_batch(ts)
        # Create oupt array to append to
        oupt_text = []
        # Reconvert tokens back and then decode array
        [oupt_text.append(self.models[f"{from_lang}-{to_lang}"]["tokenizer"].decode(self.models[f"{from_lang}-{to_lang}"]["tokenizer"].convert_tokens_to_ids(x.hypotheses[0]))) for x in results]
        return ' '.join(oupt_text)

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
        final_oupt = []
        [final_oupt.append(self.translate_single(from_lang, to_lang, inpt)) for inpt in inpt_list]
        return final_oupt

            


