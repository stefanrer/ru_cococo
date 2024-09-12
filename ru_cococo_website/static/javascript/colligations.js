import {partsTranslated, featuresTranslated, reverseDictionary} from './translations.js'

const langChangeButton = $('#language-switch');

let colligations = []

let lemmaTokenSwitchLemmaEnabledForResultTable = false;

const checkboxStates = ['TSCORE', 'DICE', 'MI'];

function setColligation(results) {
    colligations = results;
}

function drawPartsTable() {
    const items = colligations[0];
    // console.log(items);
    const partDiv = $('#part-colligation');
    partDiv.empty();

    // Starting opacity (e.g., 1.0 for 100% opacity)
    const startingOpacity = 1.0;

    for (let item = 0; item < items.length; item++) {
        const tbody = $('<tbody></tbody>').attr('id', 'Part' + item);
        tbody.attr('collapsed', true);
        partDiv.append(tbody);
        let part = items[item];

        // Calculate the new opacity, decreasing by ~5% each iteration
        let opacity = startingOpacity - (item * 0.05);

        let parameterRow = $('<tr>').attr('style', 'background-color: rgba(77, 181, 183, ' + opacity + '); border-bottom: 0.2px solid black; border-top: 0.2px solid black;').addClass('colligation-feature');

        const partName = part[1][0]['part'];
        // Translate partName if needed
        let fullPartName = '';
        if (langChangeButton.attr('data-lang') === 'ru') {
            fullPartName = reverseDictionary[partsTranslated[partName]];
        } else {
            fullPartName = partsTranslated[partName];
        }

        parameterRow.append($('<td style="width: 20%"></td>')
                    .append($('<div>')
                    .text(fullPartName)));

        const kld = part[1][0]['kld'];
        const jsd = part[1][0]['jsd'];



        parameterRow.append($('<td style="width: 20%">').text('KLD = ' + kld));
        parameterRow.append($('<td style="width: 20%">').text('JSD = ' + jsd));
        parameterRow.append($('<td style="width: 20%">'));

        tbody.append(parameterRow);

        tbody.click(function () {
            if (tbody.attr('collapsed') === "true") {
                drawKldResultTable(item);
                tbody.attr('collapsed', false);
            } else {
                $(`#Part${item} > tr:not(:first)`).remove();
                tbody.attr('collapsed', true);
            }
        })
        $(`#part-colligation > tbody:first-child`).trigger('click');
    }
}

function drawKldResultTable(item) {
    const tbody = $(`#Part${item}`);
    $(`#Part${item} > tr:not(:first)`).remove();

    let colligationData = colligations[0][item][1][0];

    // features
    colligationData.colligations.forEach(feature => {

        if (feature.feature === "variant") {
            return;
        }

        // Add Feature Header
        let featuresHeaderRaw = $('<tr>');
        featuresHeaderRaw.addClass('featureHeaderRaw');

        featuresHeaderRaw.append($('<td>'));
        featuresHeaderRaw.append($('<td>').text('Частота в корпусе'));
        featuresHeaderRaw.append($('<td>').text('Частота слова'));
        featuresHeaderRaw.append($('<td>').text('Отношение частот'));
        tbody.append(featuresHeaderRaw);



        // feature values
        feature.feature_values.forEach(param => {
            let global = param.globalCount ? param.globalCount : 0;
            let actual = param.actualCount ? param.actualCount : 0;
            let divide = actual === 0 ? 0 : actual / global;
            let newRow = $('<tr>');

            let featureValue = param.feature_value.toLowerCase();

            if (feature.feature === 'aspect') {
                if (featureValue === 'imp') {
                    featureValue = 'imperfect';
                }
            } else if (feature.feature === 'mood') {
                if (featureValue === 'imp') {
                    featureValue = 'imperative';
                }
            }

            if (langChangeButton.attr('data-lang') === 'ru') {
                featureValue = featuresTranslated[feature.feature][1][featureValue];
            }

            newRow.append($('<td>')
                    .addClass('featureValue')
                    .text(featureValue));

            newRow.append($('<td class="padding-left: 3px;">')
                    .append('<span>')
                    .text(global));

            newRow.append($('<td>')
                    .text(actual));

            newRow.append($('<td>')
                    .text((divide).toFixed(7)));

            tbody.append(newRow);
        })


        // Add Parameter Row
        let parameterRow = $('<tr>');
        parameterRow.addClass('featureRow')

        let featureName = '';

        if (langChangeButton.attr('data-lang') === 'ru') {
            featureName = featuresTranslated[feature.feature][0];
        } else {
            featureName = feature.feature;
        }

        parameterRow.append($('<td>')
                .append('<span>')
                .text(featureName));

        parameterRow.append($('<td>')
                .append('<span>')
                .text('(KLD = ' + feature.kld + ')'));

        parameterRow.append($('<td>')
                .append('<span>')
                .text('(JSD = ' + feature.jsd + ')'));

        tbody.append(parameterRow);

    });
}

function drawBigramTable(measureType = 'TSCORE',isLemmas = false) {
    const items = isLemmas ? groupWordsByLemma() :colligations[0];
    const bigramDiv = $('#colligation-words');
    bigramDiv.empty();

    const table = $('<table></table>').attr('id', 'bigramTable').addClass('bigramTable');

    const tbodyHeader = $('<tbody></tbody>').attr('id', 'bigramTableHeader');

    createBigramResultTableHeader(tbodyHeader);

    table.append(tbodyHeader);

    sortResponseWords(measureType, items);

    items.forEach(item => {
        let fullPartName = '';
        if (langChangeButton.attr('data-lang') === 'ru') {
            fullPartName = reverseDictionary[partsTranslated[item[0]]];
        } else {
            fullPartName = partsTranslated[item[0]];
        }
        const tbody = $('<tbody></tbody>').attr('id', 'part_' + item[0]);
        let visibleColumns = 7;
        let partHeader = $('<tr class="bigram-part-header"></tr>');
        partHeader.append($('<td>').append('<b>').append('<span>').text(fullPartName));
        tbody.attr('collapsed', true);
        for (let i = 0; i < visibleColumns; i++) {
            partHeader.append($('<td>').append('<b>').append('<span>'));
        }

        tbody.append(partHeader);
        const bigramData = item[1][1]
        table.append(tbody);

        partHeader.click(function () {
            if (tbody.attr('collapsed') === "true") {
                drawBigrams(tbody, bigramData);
                tbody.attr('collapsed', false);
            } else {
                $(`#part_${item[0]} > tr:not(:first)`).remove();
                tbody.attr('collapsed', true);
            }
        })
    });

    bigramDiv.append(table);
    addLemmaTokenTableSwitch(measureType);
    setCheckboxMarks(measureType);
    $(`#bigramTable > tbody:nth-child(2) > tr:first-child`).trigger('click');
}

function groupWordsByLemma() {
    function createLemmaFromToken(token) {
        let lemma = JSON.parse(JSON.stringify(token));
        lemma.word = token.lemma;
        return lemma;
}
    const groupedByLemma = [];
    colligations[0].forEach(colligation => {
        const part = colligation[0]
        const features = colligation[1][0]
        const words = colligation[1][1]

        let lemmas = []

        words.forEach(word => {
            let existingLemma = lemmas.find(o => o.word === word.lemma)
            if (!existingLemma) {
                lemmas.push(createLemmaFromToken(word))
            } else {
                existingLemma.cvalue += word.cvalue;
                existingLemma.ngramFreq += word.ngramFreq;
                existingLemma.wordFreq += word.wordFreq;
            }
        })
        groupedByLemma.push([part, [features, lemmas]])
    })
    return groupedByLemma
}

function createBigramResultTableHeader(tbody) {
    let tokenTerm, lemmaTerm, unigramTerm, ngramTerm, rankTerm;

    if (langChangeButton.attr('data-lang') === 'ru') {
        tokenTerm = 'ТОКЕН';
        lemmaTerm = 'ЛЕММА';
        unigramTerm = 'Униграмма';
        ngramTerm = 'н-грамма';
        rankTerm = 'Ранг';
    } else {
        tokenTerm = 'TOKEN';
        lemmaTerm = 'LEMMA';
        unigramTerm = 'Unigram';
        ngramTerm = 'n-gram';
        rankTerm = 'Rank';
    }

    const row = $('<tr>');

    const tokenLemmaSwitch = $('<td></td>');
    tokenLemmaSwitch.addClass('clickableTD').addClass('tokenLemmaSwitch');

    if (lemmaTokenSwitchLemmaEnabledForResultTable) {
        const tokenLemmaElement = $(`<span class="inactive">${tokenTerm}</span>/<span class="active">${lemmaTerm}</span>`);
        tokenLemmaSwitch.append(tokenLemmaElement);
    } else {
        const tokenLemmaElement = $(`<span class="active">${tokenTerm}</span>/<span class="inactive">${lemmaTerm}</span>`);
        tokenLemmaSwitch.append(tokenLemmaElement);
    }

    row.append(tokenLemmaSwitch);
    row.append($('<td>').append($('<span>').text(unigramTerm)));
    row.append($('<td>').append($('<span>').text(ngramTerm)));
    appendMeasureRadioOption(row, 'TSCORE');
    appendMeasureRadioOption(row, 'DICE');
    appendMeasureRadioOption(row, 'MI');
    row.append($('<td>').append($('<span>').addClass('sortByRank').text(rankTerm)));
    row.append($('<td>').append($('<span>').text('C-VALUE')));

    // addSortByRankListener();

    tbody.append(row);
}

function appendMeasureRadioOption(row, name) {
    let checked = checkboxStates[name];
    let td = $('<td>')
        .append($('<input>')
                .attr('type', 'checkbox')
                .attr('name', 'sortByRank')
                .attr('id', name)
                .prop('checked', checked))
                .click(function () {
                    drawBigramTable(name, lemmaTokenSwitchLemmaEnabledForResultTable)
                })
        .append($('<label>')
                .attr('style', 'cursor: pointer;')
                .attr('for', name)
                .text(name));
    row.append(td);
}

function sortResponseWords(measureType, wordsToSort) {
    function sortWordsDesc(measureType, wordsToSort) {
        wordsToSort.sort((a, b) => b.rateMap[measureType] - a.rateMap[measureType])
    }
    function sortWordsAsc(measureType, wordsToSort) {
        wordsToSort.sort((a, b) => a.rateMap[measureType] - b.rateMap[measureType])
    }
    const uppercaseValue = measureType.toUpperCase()
    wordsToSort.forEach(item => {
        const bigramData = item[1][1]
        if (measureType === 'RANK') {
            sortWordsAsc(uppercaseValue, bigramData);
        } else {
            sortWordsDesc(uppercaseValue, bigramData);
        }
    })
}

function drawBigrams(tbody, bigramData) {
    let startIndex = 0;
    const wordsLimit = 15;

    let moreTerm;

    if (langChangeButton.attr('data-lang') === 'ru') {
        moreTerm = 'Больше'
    } else {
        moreTerm = 'More'
    }

    function addBigrams(startIndex) {
        const endIndex = Math.min(startIndex + wordsLimit, bigramData.length);
        for (let i = startIndex; i < endIndex; i++) {
            const bigram = bigramData[i]
            const wordToDisplay = lemmaTokenSwitchLemmaEnabledForResultTable ? bigram.lemma : bigram.word;
            let tr = $('<tr>').attr('unigramId', bigram.unigramId).attr('style', 'padding: 9px');
            tr.append($('<td>').append('<span>').addClass('colligation-word-part').text(wordToDisplay));
            tr.append($('<td>').append('<span>').text(bigram.wordFreq));
            tr.append($('<td>').append('<span>').text(bigram.ngramFreq));
            tr.append($('<td>').append('<span>').text(bigram.rateMap['TSCORE']));
            tr.append($('<td>').append('<span>').text(bigram.rateMap['DICE']));
            tr.append($('<td>').append('<span>').text(bigram.rateMap['MI']));
            tr.append($('<td>').append('<span>').text(bigram.rateMap['RANK'] ? word.rateMap['RANK'] : ''));
            tr.append($('<td>').append('<span>').text(bigram.cvalue === 0 ? '' : bigram.cvalue));
            tbody.append(tr);
        }
        if (endIndex < bigramData.length) {
              // Add "More" button
              tbody.append($('<tr>')
                .append($('<td>')
                  .addClass('words-more-button')
                  .text(moreTerm)
                  .click(function() {
                    $(this).parent().remove(); // Remove the "More" button row
                    addBigrams(endIndex); // Add the next set of words
                  })
                )
              );
        }
    }

    addBigrams(startIndex);
}

function addLemmaTokenTableSwitch(measureType) {
    $('.tokenLemmaSwitch').click(function () {
        tokenLemmaSwitch(measureType);
    })
}

function tokenLemmaSwitch(measureType) {
    lemmaTokenSwitchLemmaEnabledForResultTable = !lemmaTokenSwitchLemmaEnabledForResultTable
    drawBigramTable(measureType, lemmaTokenSwitchLemmaEnabledForResultTable);
}

function setCheckboxMarks(measureType) {
    for (let measure in checkboxStates) {
        // console.log(checkboxStates[measure])
        // console.log(measureType)
        $('input[name="sortByRank"][id="' + checkboxStates[measure] + '"]').prop('checked', checkboxStates[measure] === measureType);
    }
}

export {setColligation, drawPartsTable, drawBigramTable};