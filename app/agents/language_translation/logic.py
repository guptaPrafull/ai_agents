from transformers import pipeline
import time
import re

# Simple sentence splitter
def sent_tokenize(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

# Translate sentence-by-sentence using dynamic lang codes
def translate_sentences(sentences, src_lang, tgt_lang, max_retries=3, wait_time=2):
    translator = pipeline(
        "translation",
        model="facebook/nllb-200-distilled-600M",
        src_lang=src_lang,
        tgt_lang=tgt_lang
    )
    translated = []
    for i, sentence in enumerate(sentences):
        retry = 0
        while retry < max_retries:
            try:
                result = translator(sentence)[0]['translation_text']
                if result.strip():
                    translated.append(result)
                    break
            except Exception as e:
                print(f"Error translating sentence {i+1}: {e}")
            retry += 1
            time.sleep(wait_time)
        else:
            translated.append("[Translation failed]")
    return translated

# Translation pipeline
def translation_pipeline(text, src_lang, tgt_lang):
    original_sentences = sent_tokenize(text)
    translated_sentences = translate_sentences(original_sentences, src_lang, tgt_lang)

    if len(original_sentences) != len(translated_sentences):
        print("Warning: Some sentences may not have been translated properly.")
        print(f"Original: {len(original_sentences)}, Translated: {len(translated_sentences)}")

    return " ".join(translated_sentences)
