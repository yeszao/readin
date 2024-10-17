from io import BytesIO

import requests
from flask import Blueprint, request, jsonify, stream_with_context, Response

from src.constants.config import DICT_API_KEY, DICT_ENDPOINT, AUDIO_ENDPOINT
from src.dao.sentence_audio_dao import SentenceAudioDao
from src.dao.sentence_dao import SentenceDao
from src.constants.languages import LANGUAGES_CODES
from src.dao.sentence_translation_dao import SentenceTranslationDao
from src.utils.auth_utils import api_login_required
from src.dto.json_dto import Json
from src.utils.openai_translator_utils import translate
from src.utils.openai_utils import get_tts

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


@bp.get('/translate')
@api_login_required
def get_translation():
    source_type = request.args.get('source_type', 0, int)
    source_id = request.args.get('source_id', 0, int)
    sentence_no = request.args.get('sentence_no', 0, int)
    to_lang = request.args.get('to_lang', '')

    if source_type not in (1, 2):
        return Json.error('Source type error!')

    if not source_id:
        return Json.error('Source id error!')

    if not sentence_no:
        return Json.error('Sentence no error!')

    if not to_lang:
        return Json.error('Language is required')

    if to_lang not in LANGUAGES_CODES:
        return Json.error('Language is not supported')

    s = SentenceDao.get_one(source_type, source_id, sentence_no)
    if not s:
        return Json.error('Sentence not found', 404)

    translation = SentenceTranslationDao.get_one(s.id, to_lang)
    if translation:
        return Json.ok({'translation': translation.translation})

    translation = translate(s.text, to_lang)
    SentenceTranslationDao.add_one(s.id, to_lang, translation)
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
        return Json.error("Play word error", response.status_code)

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    # Serve the M4A file directly from memory
    return Response(stream_with_context(generate()), content_type='audio/mp3')


@bp.get('/play/sentence')
@api_login_required
def play_sentence():
    source_type = request.args.get('source_type', 0, int)
    source_id = request.args.get('source_id', 0, int)
    sentence_no = request.args.get('sentence_no', 0, int)
    voice = request.args.get('voice')

    s = SentenceDao.get_one(source_type, source_id, sentence_no)
    if not s:
        return Json.error('Sentence not found', 404)

    audio = SentenceAudioDao.get_one(s.id, voice)
    if audio:
        def generate_from_db():
            yield from BytesIO(audio.audio)

        return Response(stream_with_context(generate_from_db()), content_type='audio/mp3')

    response = get_tts(s.text, voice)

    if response.status_code != 200:
        return Json.error("Play sentence error", response.status_code)

    audio_buffer = BytesIO()

    def generate():
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                audio_buffer.write(chunk)
                yield chunk

    streaming_response = Response(stream_with_context(generate()), content_type='audio/mp3')

    @streaming_response.call_on_close
    def on_close():
        audio_data = audio_buffer.getvalue()
        SentenceAudioDao.add_one(s.id, voice, audio_data)

    return streaming_response

