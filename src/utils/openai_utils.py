import requests

from src.constants.config import OPENAI_MODEL, OPENAI_KEY, OPENAI_TTS_MODEL

headers = {"Authorization": f"Bearer {OPENAI_KEY}"}


def get_completions(completion_params: dict) -> dict:
    completion_params.setdefault("model", OPENAI_MODEL)
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=completion_params,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["choices"][0]


def get_tts(text: str, voice: str):
    """
    https://platform.openai.com/docs/guides/text-to-speech/quickstart
    """
    params = {
        "input": text,
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "response_format": "mp3"
    }

    return requests.post("https://api.openai.com/v1/audio/speech",
                         headers=headers,
                         json=params,
                         stream=True)


if __name__ == '__main__':
    response = get_tts("who is Biden?")
    with open("output.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
