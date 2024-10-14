async function searchDictionary(offcanvasTitleEl, offcanvasContentEl, word, to_lang) {
    offcanvasTitleEl.innerHTML = word;

    const params = {
        text: word,
        to_lang: to_lang
    }

    try {
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`${DICTIONARY_URL}?${queryString}`, {"method": "GET"});

        const data = await response.json();
        if (!response.ok) {
            offcanvasContentEl.innerHTML = `<p class="text-muted">${data.error}</p>`;
            return;
        }
        displayWordDefinition(offcanvasTitleEl, offcanvasContentEl, data);
    } catch (error) {
        offcanvasContentEl.innerHTML = `<p class="text-muted">Get definition failed, please try again</p>`;
    }
}

function displayWordDefinition(offcanvasTitleEl, contentDiv, data) {
    offcanvasTitleEl.innerHTML = `${data.word}`;

    const pronunciationSection = document.createElement('div');
    data.pronunciations.forEach(pronunciation => {
        if (pronunciation.hasAudio) {
            const button = document.createElement('button');
            button.classList.add('btn', 'btn-outline-secondary', 'me-2', 'btn-sm', 'mb-2');
            button.innerHTML = `${pronunciation.accent} ${pronunciation.pronunciation} ၊၊||၊`;
            button.onclick = () => playAudio(pronunciation.id);
            pronunciationSection.appendChild(button);
        }
    });
    contentDiv.appendChild(pronunciationSection);

    // Group translations by posTag
    const groupedTranslations = data.translations.reduce((acc, {posTag, translation}) => {
        if (!acc[posTag]) {
            acc[posTag] = [];
        }
        acc[posTag].push(translation);
        return acc;
    }, {});

    // Render grouped translations
    Object.keys(groupedTranslations).forEach(posTag => {
        const groupSection = document.createElement('div');
        groupSection.innerHTML = `<p class="my-1"><span class="me-3 text-muted small">${posTag}.</span>${groupedTranslations[posTag].join(', ')}</p>`;
        contentDiv.appendChild(groupSection);
    });
}

async function translateSentence(button, sentenceText, offcanvasContentEl, toLang) {
    button.innerText = 'Translating...';
    button.disabled = true;
    try {
        // Assuming you have an API endpoint that provides the translation
        const response = await fetch(TRANSLATION_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: sentenceText,
                to_lang: toLang,
            })
        });

        const data = await response.json();
        if (!response.ok) {
            offcanvasContentEl.innerHTML = `<p class="text-muted">${data.error}</p>`;
            button.disabled = false;
            return;
        }

        offcanvasContentEl.innerHTML += '<div class="mt-3">' + data.translation + '</div>';
        button.innerText = 'Translated';
    } catch (error) {
        offcanvasContentEl.innerHTML = '<p class="text-muted">Translate failed, please try again</p>';
        button.disabled = false;
    }
}


function playAudio(pronunciationId) {
    // Assuming there's an API endpoint to fetch and play audio by pronunciation ID
    const audio = new Audio(`${PLAY_WORD_URL}?id=${pronunciationId}`);
    audio.play();
}

const initSentenceTranslation = function () {
    const sentence_btn_els = ARTICLE_CONTENT_EL.getElementsByTagName("s");

    Array.from(sentence_btn_els).forEach(function (s) {
        s.addEventListener('click', function (event) {
            s.classList.add('clicked');
            var sentenceSpanEl = event.currentTarget.parentElement;
            var sentenceText = sentenceSpanEl.querySelector('b').innerText;

            offcanvasTitleEl.innerHTML = '';
            offcanvasContentEl.innerHTML = '';

            const titleDiv = document.createElement('div');
            titleDiv.classList.add('d-flex', 'justify-content-center');

            const button = document.createElement('button');
            button.innerText = 'Translate';
            button.classList.add("btn", "btn-sm", "btn-outline-secondary", "me-2");
            titleDiv.appendChild(button);

            offcanvasTitleEl.appendChild(titleDiv);

            offcanvasContentEl.innerHTML = sentenceSpanEl.innerHTML;
            OFFCANVAS_INSTANCE.show();

            var toLang = LANGUAGE_SELECT_EL.value;
            if (!toLang) {
                alert('Please select target language at top right');
                return;
            }

            button.addEventListener('click', function () {
                translateSentence(button, sentenceText, offcanvasContentEl, toLang);
            });
        });
    });
}


const initWordTranslation = function () {
    const word_els = ARTICLE_CONTENT_EL.getElementsByTagName('i');

    Array.from(word_els).forEach(function (w) {
        w.addEventListener('click', function () {
            var toLang = LANGUAGE_SELECT_EL.value;
            if (!toLang) {
                alert('Please select target language at top right');
                return;
            }

            offcanvasTitleEl.innerHTML = 'Searching...';
            offcanvasContentEl.innerHTML = '';
            OFFCANVAS_INSTANCE.show();
            searchDictionary(offcanvasTitleEl, offcanvasContentEl, this.innerText, toLang);
        });
    });
}

function batchAction(inputList, action) {
    Array.from(inputList).forEach(item => action(item));
}

function setCookie(name, value, days) {
    let expires = "";
    let expiredDays = days || 365;

    const date = new Date();
    date.setTime(date.getTime() + (expiredDays * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();

    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const cookiesArray = document.cookie.split(';');
    for (let i = 0; i < cookiesArray.length; i++) {
        let cookie = cookiesArray[i];
        while (cookie.charAt(0) === ' ') cookie = cookie.substring(1, cookie.length);
        if (cookie.indexOf(nameEQ) === 0) return cookie.substring(nameEQ.length, cookie.length);
    }
    return null;
}

function initFontAndDarkButtons() {
    // Button elements
    const decreaseFontBtn = document.getElementById('decreaseFont');
    const increaseFontBtn = document.getElementById('increaseFont');
    const toggleDarkModeBtn = document.getElementById('toggleDarkMode');

    // Decrease font size
    decreaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize - 1;
        document.body.style.fontSize = newSize + 'px';
        setCookie('fontSize', newSize + 'px');
    });

    // Increase font size
    increaseFontBtn.addEventListener('click', () => {
        let currentSize = parseFloat(getComputedStyle(document.body).fontSize);
        let newSize = currentSize + 1;
        document.body.style.fontSize = newSize + 'px';
        setCookie('fontSize', newSize + 'px');
    });

    // Toggle dark mode
    toggleDarkModeBtn.addEventListener('click', () => {
        document.body.classList.toggle('bg-dark');
        document.body.classList.toggle('text-light');
        darkMode = document.body.classList.contains('bg-dark') ? 'dark' : 'light';
        setCookie('darkMode', darkMode);
    });
}

function initLanguageSelection() {
    const languageSelector = document.getElementById('language-selector');

    languageSelector.addEventListener('change', () => {
        setCookie('language', languageSelector.value);
    });
}

function saveReadingProgress(bookSlug, chapterNo, sentenceId) {
    const readingProgress = {
        chapterNo: chapterNo,
        sentenceId: sentenceId,
    };
    localStorage.setItem(`bookReadingProgress_${bookSlug}`, JSON.stringify(readingProgress));
}

function getReadingProgress(bookSlug) {
    return localStorage.getItem(`bookReadingProgress_${bookSlug}`);
}

function loadReadingProgressToButton(buttonSelector) {
    var readButtonEls = document.querySelectorAll(buttonSelector);
    Array.from(readButtonEls).forEach(buttonEl => {
        const bookSlug = buttonEl.dataset.bookSlug;
        const storedProgress = getReadingProgress(bookSlug);

        if (storedProgress) {
            const {chapterNo, sentenceId} = JSON.parse(storedProgress);
            buttonEl.href = `/${bookSlug}/${chapterNo}.html#${sentenceId}`;
            buttonEl.innerText = `Continue Reading`;
        }
    });
}

function getFirstVisibleSentenceId() {
    // Get all <s> tags on the page
    const sTags = document.querySelectorAll('s');

    // Loop through the <s> tags to find the first visible one
    for (let sTag of sTags) {
        const rect = sTag.getBoundingClientRect();

        // Check if the element is in the visible window (partially or fully)
        if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
            // Return the id of the first visible <s> tag
            return sTag.id;
        }
    }

    return 1;
}
