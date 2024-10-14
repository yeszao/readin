import requests
from flask import Blueprint, request, jsonify, stream_with_context, Response

from src.constants.config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT
from src.db.sentence_dao import SentenceDao
from src.constants.languages import LANGUAGES_CODES
from src.utils.auth_utils import api_login_required
from src.utils.json_utils import Json
from src.utils.openai_translator_utils import translate

bp = Blueprint('tool', __name__)


@bp.get('/dictionary')
@api_login_required
def get_dictionary():
    from_lang = request.args.get('from_lang', 'en')
    to_lang = request.args.get('to_lang')
    text = request.args.get('text')

    if to_lang is None:
        return jsonify({'error': 'Language is required'}), 400

    if text is None:
        return jsonify({'error': 'Translate text is required'}), 400

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {
        'from_lang': from_lang,
        'to_lang': to_lang,
        'text': text
    }
    response = requests.get(headers=headers, url=DICT_ENDPOINT, params=params)
    if response.status_code != 200:
        return Json.error(response.json()['detail'], response.status_code)

    return Json.ok(response.json())


@bp.post('/translate')
@api_login_required
def get_translation():
    text = request.json.get('text')
    to_lang = request.json.get('to_lang')

    if text is None:
        return Json.error('Text is required')

    if to_lang is None:
        return Json.error('Language is required')

    if to_lang not in LANGUAGES_CODES:
        return Json.error('Language is not supported')

    s = SentenceDao.get_one(text, to_lang)
    if s:
        return Json.ok({'translation': s.translation})

    translation = translate(text, to_lang)
    SentenceDao.add_one(text, to_lang, translation)
    return Json.ok({'translation': translation})


@bp.get('/play/word')
@api_login_required
def play_word():
    pronunciation_id = request.args.get('id')

    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': DICT_API_KEY,
    }
    params = {'pronunciation_id': pronunciation_id}
    response = requests.get(headers=headers, url=AUDIO_ENDPOINT, params=params, stream=True)

    # Check if the response is valid and contains MP3 data
    if response.status_code != 200:
        return "Audio file not found", 404

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    # Serve the M4A file directly from memory
    return Response(stream_with_context(generate()), content_type='audio/mp3')

