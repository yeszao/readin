from bs4 import BeautifulSoup

from src.dto.html_dto import ParsedHtml, SentenceWords
from src.utils.nlp_utils import nlp_get_words, nlp_get_sentences

ALLOWED_TAGS = {'h1', 'h2', 'p', 'ul', 'li', 'ol', 'blockquote', 'i', 'em', 'br', 'b', 'hr'}


def check_tags(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    unexpected_tags = set()
    for tag in soup.find_all(True):  # True finds all tags
        if tag.name not in ALLOWED_TAGS:
            unexpected_tags.add(tag.name)

    return unexpected_tags


def tagged_html(input_html: str) -> ParsedHtml:
    soup = BeautifulSoup(input_html, 'html.parser')
    parsed = ParsedHtml()

    sentence_no = 0
    for tag in soup.find_all(['p', 'span', 'li', 'h2', 'h3', 'h4', 'h5']):
        tag.attrs = {}
        try:
            sentence_no = _process_tag(tag, sentence_no, parsed)
        except Exception as e:
            print(f'Error processing tag: {e}')
            continue

    parsed.tagged_content_html = str(soup)
    parsed.vocabulary_count = len(parsed.vocabulary)
    return parsed


def _process_tag(tag, sentence_no, parsed) -> int:
    plain_text = tag.get_text().strip()
    if plain_text.strip() == '':
        return sentence_no

    sentences = nlp_get_sentences(plain_text)
    tagged_sentences = []

    for s in sentences:
        sentence_no += 1

        wrapped, vocabulary_set, word_count = wrap_words(s)
        parsed.vocabulary.update(vocabulary_set)
        parsed.sentences.append(SentenceWords(no=sentence_no, text=s, words=vocabulary_set))
        parsed.word_count += word_count
        parsed.sentence_count += 1

        tagged_sentences.append(f'<span><s>{sentence_no}</s><b>{wrapped}</b></span>')

    tag.clear()
    tag.append(BeautifulSoup(' '.join(tagged_sentences), 'html.parser'))

    return sentence_no


def wrap_title(title: str) -> str:
    wrapped, _, _ = wrap_words(title)
    return f'<span><b>{wrapped}</b></span>'


def wrap_words(text, start_tag='<i>', end_tag='</i>') -> (str, int, int):
    doc = nlp_get_words(text)
    wrapped = ''
    vocabulary_set = set()
    word_count = 0

    for token in doc:
        if token.is_alpha:
            vocabulary_set.add(token.text.lower())
            word_count += 1
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped, vocabulary_set, word_count
