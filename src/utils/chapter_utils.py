from typing import List, Set, Tuple, Dict
import spacy
from bs4 import BeautifulSoup
from spacy.language import Language

nlp: Language = spacy.load("en_core_web_sm")
ALLOWED_TAGS = {'h1', 'h2', 'p', 'ul', 'li', 'ol', 'blockquote', 'i', 'em', 'br', 'b', 'hr'}


def _get_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


def _get_words(text: str):
    return nlp(text)


def check_tags(input_html):
    soup = BeautifulSoup(input_html, 'html.parser')
    unexpected_tags = set()
    for tag in soup.find_all(True):  # True finds all tags
        if tag.name not in ALLOWED_TAGS:
            unexpected_tags.add(tag.name)

    return unexpected_tags


def tagged_html(input_html: str) -> (str, List[Tuple[int, str, list]], Set[str], int):
    soup = BeautifulSoup(input_html, 'html.parser')

    all_sentences = []
    sentence_no = 0
    all_vocabulary = set()
    all_word_count = 0
    for tag in soup.find_all(['p', 'span', 'li', 'h2', 'h3', 'h4', 'h5']):
        tag.attrs = {}
        try:
            sentence_no, sentences, sentence_word_count = _process_tag(tag, sentence_no, all_vocabulary)
        except Exception as e:
            print(f'Error processing tag: {e}')
            continue
        all_word_count += sentence_word_count
        all_sentences.extend(sentences)

    content = str(soup)
    return content, all_sentences, all_vocabulary, all_word_count


def _process_tag(tag, sentence_no, all_vocabulary) -> (int, List[Tuple[int, str, list]], int):
    tag_sentences = []  # [(sentence_no, sentence, vocabulary), (...), ...]
    plain_text = tag.get_text().strip()
    if plain_text.strip() == '':
        return sentence_no, tag_sentences, 0

    sentences = _get_sentences(plain_text)
    tagged_sentences = []
    sentence_word_count = 0

    for s in sentences:
        sentence_no += 1
        wrapped, vocabulary, word_count = wrap_words(s)
        all_vocabulary.update(vocabulary)
        tag_sentences.append((sentence_no, s, vocabulary))
        sentence_word_count += word_count
        tagged_sentences.append(f'<span><s>{sentence_no}</s><b>{wrapped}</b></span> ')

    tag.clear()
    tag.append(BeautifulSoup(' '.join(tagged_sentences), 'html.parser'))

    return sentence_no, tag_sentences, sentence_word_count


def wrap_words(text, start_tag='<i>', end_tag='</i>') -> (str, int, int):
    doc = _get_words(text)
    wrapped = ''
    vocabulary = set()
    word_count = 0

    for token in doc:
        if token.is_alpha:
            vocabulary.add(token.text.lower())
            word_count += 1
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped, vocabulary, word_count


def wrap_words_and_entities(text, start_tag='<i>', end_tag='</i>'):
    doc = _get_words(text)
    wrapped = ''

    # Merge entities (such as "New York" or "John Smith") into single tokens
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)

    for token in doc:
        if token.is_alpha or token.ent_type_:
            wrapped += f'{start_tag}{token.text}{end_tag}'
        else:
            # Keep punctuation and non-alpha tokens unchanged
            wrapped += token.text

        if token.whitespace_:
            wrapped += token.whitespace_

    return wrapped
