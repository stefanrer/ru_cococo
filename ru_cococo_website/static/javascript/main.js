import {allFeatures, features} from './morphology.js'
import {setCollocations, drawResults} from "./collocations.js";
import {setColligation, drawPartsTable, drawBigramTable} from './colligations.js'

const langChangeButton = $('#language-switch');

let searchForLemma1 = false;
let searchForLemma2 = false;
let searchForLemma3 = false;
let searchForLemma4 = false;

let amountOfFilters = 2;

let morphologyFeats = ["", "", "", ""]

$(document).ready(function () {

    // $('#delete-on-launch').remove();

    addSpinnerOnLoading();

    const filter1 = $('#search-filter1');
    const filter2 = $('#search-filter2');
    const filter3 = $('#search-filter3');
    const filter4 = $('#search-filter4');

    filter3.hide();
    filter4.hide();

    const partSelect1 = $('#part-select1');
    const partSelect2 = $('#part-select2');
    const partSelect3 = $('#part-select3');
    const partSelect4 = $('#part-select4');

    const showFeatsButton1 = $('#show-feats1');
    const showFeatsButton2 = $('#show-feats2');
    const showFeatsButton3 = $('#show-feats3');
    const showFeatsButton4 = $('#show-feats4');

    showFeatsButton1.hide();
    showFeatsButton2.hide();
    showFeatsButton3.hide();
    showFeatsButton4.hide();

    const lemmaToggle1 = $('#lemma-toggle1');
    const lemmaToggle2 = $('#lemma-toggle2');
    const lemmaToggle3 = $('#lemma-toggle3');
    const lemmaToggle4 = $('#lemma-toggle4');

    const plusButton = $('#plus-button');
    const minusButton = $('#minus-button');
    const searchButton = $('#search-button');
    const resetButton = $('#reset-button');

    minusButton.hide();

    plusButton.click(function () {
        if (amountOfFilters === 2) {
            amountOfFilters = 3
            filter3.show()
            minusButton.show()
        } else if (amountOfFilters === 3) {
            amountOfFilters = 4
            filter4.show()
            minusButton.show()
            plusButton.hide()
        }
        $('#collocation-results').empty();
    });

    minusButton.click(function () {
        if (amountOfFilters === 4) {
            morphologyFeats[3] = ""
            amountOfFilters = 3
            filter4.hide()
            plusButton.show()
        } else if (amountOfFilters === 3) {
            amountOfFilters = 2
            morphologyFeats[2] = ""
            filter3.hide()
            plusButton.show()
            minusButton.hide()
        }
        $('#collocation-results').empty();
    });

    searchButton.click(search);

    //Search on Enter click
    $('.search-banner').keypress(function (e) {
        if (e.which === 13) {
            searchButton.trigger('click');
            return false;
        }
    });

    resetButton.click(function () {
        location.reload()
    });


    partSelect1.change(() => {
        morphologyFeats[0] = "";
        const value = partSelect1.val();
        if (value === 'all') {
            showFeatsButton1.hide();
        }
        else {
            if (value in features) {
                showFeatsButton1.show();
            } else {
                showFeatsButton1.hide();
            }
        }
    });

    partSelect2.change(() => {
        morphologyFeats[1] = "";
        const value = partSelect2.val();
        if (value === 'all') {
            showFeatsButton2.hide();
        }
        else {
            if (value in features) {
                showFeatsButton2.show();
            } else {
                showFeatsButton2.hide();
            }
        }
    });

    partSelect3.change(() => {
        morphologyFeats[2] = "";
        const value = partSelect3.val();
        if (value === 'all') {
            showFeatsButton3.hide();
        }
        else {
            if (value in features) {
                showFeatsButton3.show();
            } else {
                showFeatsButton3.hide();
            }
        }
    });

    partSelect4.change(() => {
        morphologyFeats[3] = "";
        const value = partSelect4.val();
        if (value === 'all') {
            showFeatsButton4.hide();
        }
        else {
            if (value in features) {
                showFeatsButton4.show();
            } else {
                showFeatsButton4.hide();
            }
        }
    });





    lemmaToggle1.click(function () {
        searchForLemma1 = !searchForLemma1;
        console.log(searchForLemma1);
    });

    lemmaToggle2.click(function () {
        searchForLemma2 = !searchForLemma2;
        console.log(searchForLemma2);
    });

    lemmaToggle3.click(function () {
        searchForLemma3 = !searchForLemma3;
        console.log(searchForLemma3);
    });

    lemmaToggle4.click(function () {
        searchForLemma4 = !searchForLemma4;
        console.log(searchForLemma4);
    });

    showFeatsButton1.click(function () {
        drawMorphFeatures(partSelect1, 0);
    });

    showFeatsButton2.click(function () {
        drawMorphFeatures(partSelect2, 1);
    });

    showFeatsButton3.click(function () {
        drawMorphFeatures(partSelect3, 2);
    });

    showFeatsButton4.click(function () {
        drawMorphFeatures(partSelect4, 3);
    });
});

function addSpinnerOnLoading() {
    $(document).on({
        ajaxStart: function () {
            $('body').addClass('loading');
        },
        ajaxStop:  function () {
            $('body').removeClass('loading');
        }
    });
}

function drawMorphFeatures(selectedPart, morphologyFeatsNum) {
    const body = $('body');
    const morphology = $('<div></div>').addClass('morphology-settings-window').attr('id', `morphology-settings-window-${morphologyFeatsNum}`);
    const morphologyContent = $('<div></div>').addClass('morphology-settings-content');
    const morphologyFilters = $('<div></div>').addClass('morphology-filters');
    const morphologyFooter = $('<div></div>').addClass('morphology-footer');
    const featTable = $('<div></div>').addClass('feat-table').attr('id', 'feat-table');
    morphologyFilters.append(featTable);
    morphologyContent.append(morphologyFilters, morphologyFooter);
    morphology.append(morphologyContent);
    body.append(morphology);

    const availableFeatures = features[selectedPart.val()];
    if (!availableFeatures) {
        console.log('No features available')
    }

    let okTerm, cancelTerm;

    if (langChangeButton.attr('data-lang') === 'ru') {
        okTerm = 'Ок';
        cancelTerm = 'Отмена';
    } else {
        okTerm = 'Ok';
        cancelTerm = 'Cancel';
    }

    let selectedFeatures = getSelectedFeatures(morphologyFeats[morphologyFeatsNum]);

    availableFeatures.forEach(feature => {
       const featureDiv = $('<div></div>').attr('style', 'padding: 15px');
       featTable.append(featureDiv);

       featureDiv.append($('<div></div>')
                .text(langChangeButton.attr('data-lang') === 'ru'? feature.title : feature.name) // set either title on name depending on lang
                .addClass('feature-label'));

       const inputsDiv = $('<div class="features-inputs">');
       featureDiv.append(inputsDiv);

       let featureSelectedValues = feature.name in selectedFeatures ? selectedFeatures[feature.name]: [];

       feature.values.forEach(featureValue => {
           const featureInputDiv = $('<div></div>').addClass('feature-input');
           const id = feature.name + '_' + featureValue.value;
           const input = $('<input>')
               .attr('type', 'checkbox')
               .attr('value', featureValue.value)
               .attr('id', id)
               .attr('name', feature.name)
               .attr('checked', featureSelectedValues.some(value => value === featureValue.value));

           const inputLabel = $('<label>').attr('for', id);
           inputLabel.text(langChangeButton.attr('data-lang') === 'ru'? featureValue.title : featureValue.value); // set either title on name depending on lang
           featureInputDiv.append(input, inputLabel);

           inputsDiv.append(featureInputDiv)
       });
    });
    const morphologyButtons = $('<div></div>').addClass('morphology-buttons')
    const enterButton = $('<div></div>')
        .addClass('co-button enter-button')
        .attr('id', 'morphology-enter-button')
        .text(okTerm);
    const cancelButton = $('<div></div>')
        .addClass('co-button cancel-button')
        .attr('id', 'morphology-cancel-button')
        .text(cancelTerm);
    morphologyButtons.append(enterButton, cancelButton);
    morphologyFooter.append(morphologyButtons);

    cancelButton.click(function () {
        $('#feat-table input:checkbox').prop('checked', false);
    });

    enterButton.click(function () {
        morphologyFeats[morphologyFeatsNum] = getFeats();
        morphology.remove();
    });
}

function getSelectedFeatures(morphFeats) {
    let selectedFeatures = {};
    if (morphFeats === "") {
        return selectedFeatures;
    }
    const keyValuePairs = morphFeats.split(";");
    for (const pair of keyValuePairs) {
        const [key, valueString] = pair.split(":");
        if (valueString) {
            const values = valueString.split(",");
            selectedFeatures[key] = values;
        }
    }
    return selectedFeatures;
}

function getFeats() {
    let selectedFilters = [];
    $('#feat-table input:checkbox:checked').each(function () {
        let input = {
            name:  $(this).attr('name'),
            value: $(this).val()
        }
        selectedFilters.push(input);
    });
    // console.log(selectedFilters);
    let result = selectedFilters.reduce(function (r, a) {
        r[a.name] = r[a.name] || [];
        r[a.name].push(a.value);
        return r;
    }, Object.create(null));

    let resultQuery = '';
    for (const item in result) {
        resultQuery = resultQuery + item + ':' + result[item].join(',') + ';'
    }

    return resultQuery;
}

function search(e) {
    const word1 = $('#word1').val().trim();
    const word2 = $('#word2').val().trim();
    const word3 = $('#word3').val().trim();
    const word4 = $('#word4').val().trim();

    // console.log(word1, word2, word3, word4);

    const part1 = $('select[name=part1]').val();
    const part2 = $('select[name=part2]').val();
    const part3 = $('select[name=part3]').val();
    const part4 = $('select[name=part4]').val();

    // console.log(part1, part2, part3, part4);

    const filter1 = morphologyFeats[0];
    const filter2 = morphologyFeats[1];
    const filter3 = morphologyFeats[2];
    const filter4 = morphologyFeats[3];

    // console.log(filter1, filter2, filter3, filter4);

    // Check if checkbox is checked
    const advanced = $('#advancedSearch').is(':checked');

    drawUserReadableQuery();

    $.ajax({
        url:    '/public/api/search',
        type:   'GET',
        data:   {
            measureType: 'TSCORE',
            word1:  word1,
            part1:  part1,
            filter1:   filter1,
            isLemma1: searchForLemma1,
            word2:  word2,
            part2:  part2,
            filter2:   filter2,
            isLemma2: searchForLemma2,
            word3:  word3,
            part3:  part3,
            filter3:   filter3,
            isLemma3: searchForLemma3,
            word4: word4,
            part4: part4,
            filter4: filter4,
            isLemma4: searchForLemma4,
            nGrams: amountOfFilters,
            advanced: advanced,
        },
        timeout: 60 * 1000,
        success: function (results) {
            const resultsDiv = $('#results');
            resultsDiv.empty();

            if (advanced) {
                colligation(resultsDiv, results);
            } else {
                collocation(resultsDiv, results, [word1, word2, word3, word4]);
            }
        }
    }).fail(function (jqXHR, textStatus) {
        if (textStatus === 'timeout') {
            alert('Превышен лимит времени на выполнение запроса');
            //do something. Try again perhaps?
        }
    });
}

function colligation(resultsDiv, results) {
    if (results.every(item => item.length === 0)) {
        console.log("Colligations not found");
        return;
    }
    const colligationDiv = $('<div class="colligation-results" id="colligation-results"></div>')
    const partDiv = $('<div class="part-colligation" id="part-colligation"></div>');
    const bigramDiv = $('<div class="colligation-words" id="colligation-words"></div>');

    colligationDiv.append(partDiv, bigramDiv);
    resultsDiv.append(colligationDiv);

    setColligation(results);
    drawPartsTable();
    drawBigramTable();
}

function collocation(resultsDiv, results, words) {
    if (results.every(item => item.length === 0)) {
        console.log("Collocations not found");
        return;
    }
    const collocationResultsDiv = $('<div class="collocation-results" id="collocation-results"></div>');
    resultsDiv.append(collocationResultsDiv);

    setCollocations(results);

    let unigram_places = []
    if (words[0] === '') {
        unigram_places.push(1)
    }
    if (amountOfFilters >= 2 && words[1] === '') {
        unigram_places.push(2)
    }
    if (amountOfFilters >= 3 && words[2] === '') {
        unigram_places.push(3)
    }
    if (amountOfFilters === 4 && words[3] === '') {
        unigram_places.push(4)
    }

    drawResults(collocationResultsDiv, unigram_places.length, unigram_places)
}

function drawUserReadableQuery() {
    let finalQuery = "";
    for (let filter = 1; filter <= amountOfFilters; filter++) {
        if (filter !== 1) {
            finalQuery += ' + '
        }
        // Get word value
        const word = $(`#word${filter}`).val();
        // Get word part value
        let part = $(`select[name=part${filter}]`).val();
        part = `[${part}]`;
        // Get word part features
        let feats = morphologyFeats[filter-1]
        if (feats.length !== 0) {
            feats = `(${feats})`;
        } else {
            feats = "";
        }
        const query = word + part + feats
        // console.log(query)
        finalQuery += query
    }
    // console.log(finalQuery);
    $('#user-query').text(finalQuery);
}