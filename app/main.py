from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from translate import Translator
import logging
from languagecode import iso_639_choices

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranslationRequest(BaseModel):
    source_lang: str
    target_lang: str
    text: str


class TranslationResponse(BaseModel):
    source_lang: str
    target_lang: str
    text: str
    translated_text: str


class SupportedLanguagesResponse(BaseModel):
    supported_languages: list


@app.post("/translate")
async def translate_text(request_data: TranslationRequest):
    try:
        source_lang = request_data.source_lang
        target_lang = request_data.target_lang
        text = request_data.text

        if not source_lang or not target_lang or not text:
            raise HTTPException(status_code=400, detail="Invalid input parameters")

        translator = Translator(to_lang=target_lang, from_lang=source_lang)
        translated_text = translator.translate(text)

        logger.info(f"Translation request: {text} ({source_lang} to {target_lang})")

        return TranslationResponse(source_lang=source_lang, target_lang=target_lang, text=text,
                                   translated_text=translated_text)
    except Exception as e:

        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@app.get("/languages")
async def get_supported_languages():
    try:

        supported_languages = [{"code": code, "name": name} for code, name in iso_639_choices]
        return SupportedLanguagesResponse(supported_languages=supported_languages)
    except Exception as e:

        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting supported languages: {str(e)}")
