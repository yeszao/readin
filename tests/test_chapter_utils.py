import pytest

from src.dto.html_dto import SentenceWords
from src.utils.html_utils import tagged_html, wrap_words
from tests import TEST_FILES_DIR

input_file = TEST_FILES_DIR.joinpath("chapter_utils").joinpath('chapter.html')


def test_tagged_html():
    input_html = input_file.read_text()
    parsed = tagged_html(input_html)
    assert parsed.sentence_count == 14
    assert len(parsed.tagged_content_html) > 0
    assert 'callMontauk' not in parsed.tagged_content_html
    assert parsed.vocabulary_count == 168
    assert parsed.word_count == 271


@pytest.mark.parametrize(
    "html, tagged_content_html, sentence_count, word_count, vocabulary_count, sentences, vocabulary", [
        ("", "", 0, 0, 0, [], set()),
        ("<p></p>", "<p></p>", 0, 0, 0, [], set()),
        ("<p>Hello World. I am good!</p><ul><li>This is one</li><li>This is Two.</li></ul>",
         '<p><span><s>1</s><b><i>Hello</i> <i>World</i>.</b></span> <span><s>2</s><b><i>I</i> <i>am</i> <i>good</i>!</b></span></p><ul><li><span><s>3</s><b><i>This</i> <i>is</i> <i>one</i></b></span></li><li><span><s>4</s><b><i>This</i> <i>is</i> <i>Two</i>.</b></span></li></ul>',
         4,
         11,
         9,
         [{'no': 1, 'text': 'Hello World.', 'words': {'hello', 'world'}},
          {'no': 2, 'text': 'I am good!', 'words': {'i', 'am', 'good'}},
          {'no': 3, 'text': 'This is one', 'words': {'this', 'is', 'one'}},
          {'no': 4, 'text': 'This is Two.', 'words': {'this', 'is', 'two'}}],
         {'hello', 'world', 'i', 'am', 'good', 'this', 'is', 'one', 'two'}),
    ])
def test_tagged_html2(html, tagged_content_html, sentence_count, word_count, vocabulary_count, sentences, vocabulary):
    result = tagged_html(html)
    assert result.tagged_content_html == tagged_content_html
    assert result.sentence_count == sentence_count
    assert result.word_count == word_count
    assert result.vocabulary_count == vocabulary_count
    assert result.sentences == [SentenceWords(**s) for s in sentences]
    assert result.vocabulary == vocabulary


@pytest.mark.parametrize("text, expected", [
    ("Hello, world!", ('[Hello], [world]!', 2, 2)),
    ("I love Perter's laptop.", ('[I] [love] [Perter]\'s [laptop].', 4, 4)),
    ("John Smith was born in New York but moved to Los Angeles in United States.", (
            '[John] [Smith] [was] [born] [in] [New] [York] [but] [moved] [to] [Los] [Angeles] [in] [United] [States].',
            14,
            15)),
])
def test_wrap_words(text, expected):
    wrapped, vocabulary, word_count = wrap_words(text, '[', ']')
    assert (wrapped, len(vocabulary), word_count) == expected
