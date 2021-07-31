
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class LanguageTranslation:
    def __init__(self, gpu, model_prefix_name, languages_supported, models):
        self.gpu = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model_prefix_name = "Helsinki-NLP/opus-mt-"
        self.languages_supported = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it"
        }
        self.models = {}
    
    def load_tokenizer(from_lang: str, to_lang: str):
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
        model_string_name = f"{self.model_prefix_name}{from_lang}-{to_lang}"
        return AutoTokenizer.from_pretrained(model_string_name)

    def load_model(from_lang: str, to_lang: str):
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
        model_string_name = f"{self.model_prefix_name}{from_lang}-{to_lang}"
        return AutoModelForSeq2SeqLM.from_pretrained(model_string_name).to(self.gpu)

    def load_languages(lang_list: list):
        '''
        desc:
            Given list of languages to be able to translate, load the tokenizer/models
            into the self.models dict to be referenced downstream.
            Only supports translating to English currently.
        inpt:
            lang_list [list]: list of language abbreviations to be able to translate from.
        oupt:
            self.models [dict]: updated with tokenizer/model combos from lang_list.
        '''
        all_models = {}
        for k,v in self.languages_supported.iteritems():
            if k != "English":
                self.models[f"{k}-en"]["tokenizer"] = load_tokenizer(k, "en")
                self.models[f"{k}-en"]["model"] = load_model(k, "en")

    def translate_single(from_lang: str, to_lang: str, text: str) -> str:
        '''
        '''
        tokenized_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"].prepare_seq2seq_batch([text], return_tensors = "pt").to(self.gpu)
        translated_tokens = self.models[f"{from_lang}-{to_lang}"]["model"].generate(**tokenized_text)
        translated_text = self.models[f"{from_lang}-{to_lang}"]["tokenizer"].batch_decode(translated_tokens, skip_special_tokens = True)
        torch.cuda.empty_cache()
        return translated_text

    def translate_batch(inpt_list: list):
        '''
        '''
        oupt = []
        foreign_lang_list = list(set([x["from_lang"] for x in inpt_list]))
        inpt_dict = {}
        for lang in foreign_lang_list:
            inpt_dict[lang] = [x for x in inpt_list if x["from_lang"] == lang]
        for lang, text_list_dict in inpt_dict.iteritems():
            text_list = [x["text"] for x in text_list]
        return oupt
            


