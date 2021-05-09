from text2text import TextGenerator
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator(TextGenerator):
  pretrained_model_path = "facebook/m2m100_1.2B"

  def __init__(self, **kwargs):
    pretrained_model_path = kwargs.get('pretrained_model_path')
    if not pretrained_model_path:
      pretrained_model_path = self.__class__.pretrained_model_path
    self.__class__.model = AutoModelForSeq2SeqLM.from_pretrained(pretrained_model_path)
    self.__class__.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_path)

  def _translate(self, input_lines, src_lang='en', **kwargs):
    tokenizer = self.__class__.tokenizer
    tokenizer.src_lang = src_lang
    if 'tgt_lang' not in kwargs:
      raise ValueError('tgt_lang not specified')
    tgt_lang = kwargs.get('tgt_lang')
    if tgt_lang not in self.__class__.LANGUAGES:
      raise ValueError(f'{tgt_lang} not found in {self.__class__.LANGUAGES}')
    encoded_inputs = tokenizer(input_lines, padding=True, return_tensors="pt")
    tgt_token_id = tokenizer.lang_code_to_id[tgt_lang]
    generated_tokens = self.__class__.model.generate(**encoded_inputs, forced_bos_token_id=tgt_token_id)
    return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True) 

  def predict(self, input_lines, src_lang='en', **kwargs):
    TextGenerator.predict(self, input_lines, src_lang=src_lang, **kwargs)
    return self._translate(input_lines, src_lang=src_lang, **kwargs)