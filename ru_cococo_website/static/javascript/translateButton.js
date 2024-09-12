import {translateDictionary, reverseDictionary, parts, partsTranslated} from './translations.js'

$(document).ready(function () {

    const langChangeButton = $('#language-switch');

    if (langChangeButton.attr('data-lang') === 'en') {
        localize();
    }

    langChangeButton.click(function () {
        localizeButton();
    });


    function localize() {
        function replaceText(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                let text = node.nodeValue.trim();
                if (translateDictionary[text]) {
                    node.nodeValue = translateDictionary[text];
                } else if (reverseDictionary[text]) {
                    node.nodeValue = reverseDictionary[text];
                }
            } else if (node.nodeType === Node.ELEMENT_NODE && node.getAttribute('placeholder')) {
                let placeholderText = node.getAttribute('placeholder').trim();
                if (translateDictionary[placeholderText]) {
                    node.setAttribute('placeholder', translateDictionary[placeholderText]);
                } else if (reverseDictionary[placeholderText]) {
                    node.setAttribute('placeholder', reverseDictionary[placeholderText]);
                }
            } else {
                node.childNodes.forEach(replaceText);
            }
        }

        // Replace text on the entire page
        document.body.childNodes.forEach(replaceText);
    }

    // Function to replace/translate text
    function localizeButton() {
        function replaceText(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                let text = node.nodeValue.trim();
                if (translateDictionary[text]) {
                    node.nodeValue = translateDictionary[text];
                } else if (reverseDictionary[text]) {
                    node.nodeValue = reverseDictionary[text];
                }
            } else if (node.nodeType === Node.ELEMENT_NODE && node.getAttribute('placeholder')) {
                let placeholderText = node.getAttribute('placeholder').trim();
                if (translateDictionary[placeholderText]) {
                    node.setAttribute('placeholder', translateDictionary[placeholderText]);
                } else if (reverseDictionary[placeholderText]) {
                    node.setAttribute('placeholder', reverseDictionary[placeholderText]);
                }
            } else if (node.classList.contains('colligation-word-part') || node.classList.contains('word-part')) {
            } else {
                    node.childNodes.forEach(replaceText);
                }
        }

        let lang = langChangeButton.attr('data-lang')

        $.ajax({
            url: '/change_lang/' + lang,
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    console.log("function done")
                    if (lang === 'ru') {
                        console.log('Switch to ENG');
                        langChangeButton.attr('data-lang', 'en');
                    } else {
                        console.log('Switch to RU');
                        langChangeButton.attr('data-lang', 'ru');
                    }
                    // Replace text on the entire page
                    document.body.childNodes.forEach(replaceText);
                }
            }
        }).fail(function (jqXHR, textStatus) {
            alert('failed translation')
        });
    }
});