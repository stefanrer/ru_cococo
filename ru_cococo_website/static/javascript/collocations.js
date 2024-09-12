import {parts, partsTranslated} from "./translations.js";

let collocations = [];

const langChangeButton = $('#language-switch');

let lemmaTokenSwitchLemmaEnabledForResultTable = [false, false, false]

function setCollocations(results) {
    collocations = results;
}

function drawResults(resultDiv, numTables, unigram_places) {
    for (let table_num = 0; table_num < numTables; table_num++) {
        // Create a new table
        const table = $('<table></table>').attr('id', 'resultTable' + table_num).addClass('resultTable')

        // Create a new tbody for lemma switch
        const tbody = $('<tbody></tbody>');

        // Append the tbody to the table
        table.append(tbody);

        adjustTable(unigram_places[table_num], table.get(0));

        window.addEventListener('resize', () => {
            adjustTable(unigram_places[table_num], table.get(0));
        });

        if (!($(`#tableLemmaToggle${table_num + 1}`).length)) {
            createResultTableHeader(tbody, table_num)
        }

        // Append the table to the div
        resultDiv.append(table).show();

        drawTableResults(table_num)
    }
}

function drawTableResults(table_num, measureType = 'TSCORE') {
    const table = $('#resultTable' + table_num)
    $('#resultTable' + table_num + ' tbody:not(:first)').remove();
    const maxRate = calculateMaxRate(collocations[table_num], measureType);
    collocations[table_num].forEach(item => {
        const partTbody = $('<tbody></tbody>');
        addHeaderRaw(partTbody, item.part, true);
        if (!lemmaTokenSwitchLemmaEnabledForResultTable[table_num]) {
            addWordsToResultTableHeader(partTbody, item.unigrams, maxRate, table_num, measureType)
        } else {
            console.log('Lemmas')
            let unique_lemmas = createUniqueLemmas(item.unigrams, measureType)
            addWordsToResultTableHeader(partTbody, unique_lemmas, maxRate, table_num, measureType)
        }
        table.append(partTbody);
    })
}

function createUniqueLemmas(values, measureType = 'TSCORE') {
    let lemmaDict = {};
        values.forEach(unigram => {
            let lemma = unigram.lemma;
            if (!(lemma in lemmaDict) || unigram.rateMap[measureType] > lemmaDict[lemma].rateMap[measureType]) { //
                lemmaDict[lemma] = unigram;
            }
        })
    // Convert the dictionary values to a list
    return Object.values(lemmaDict)
}

function addWordsToResultTableHeader(tbody, words_to_add, maxRate, table_num, measureType = 'TSCORE') {
    let startIndex = 0;
    const wordsLimit = 15;

    let moreTerm;

    if (langChangeButton.attr('data-lang') === 'ru') {
        moreTerm = 'Больше'
    } else {
        moreTerm = 'More'
    }

    function addWords(startIndex) {
        const endIndex = Math.min(startIndex + wordsLimit, words_to_add.length);
        for (let i = startIndex; i < endIndex; i++) {
          const word = words_to_add[i];
          const wordToDisplay = lemmaTokenSwitchLemmaEnabledForResultTable[table_num] ? word.lemma : word.word;
          const opacity = getOpacity(maxRate, word.rateMap[measureType]);
          tbody.append($('<tr>')
            .attr('unigramId', word.unigramId)
            .attr('style', 'background-color: rgb(77, 181, 183, ' + opacity + '); padding: 9px')
            .addClass('part-body')
            .append($('<td style="padding-left: 0.2em;">')
              .addClass('word-part')
              .append('<span>')
              .text(wordToDisplay))
          );
        }

        if (endIndex < words_to_add.length) {
          // Add "More" button
          tbody.append($('<tr>')
            .append($('<td>')
              .addClass('words-more-button')
              .text(moreTerm)
              .click(function() {
                $(this).parent().remove(); // Remove the "More" button row
                addWords(endIndex); // Add the next set of words
              })
            )
          );
        }
    }

  addWords(startIndex); // Initial call to add the first set of words
}

function getOpacity(maxValue, currentValue) {
    return (currentValue / maxValue) ;
}

function addHeaderRaw(tbody, text, isUpperCase) {
    if (langChangeButton.attr('data-lang') === 'ru') {
        console.log("translate part to ru")
        text = parts[text]
    } else {
        console.log("translate part to en")
        text = partsTranslated[text]
    }
    let clusterHeader = $('<tr>');
    if (isUpperCase) {
        clusterHeader.attr('style', 'text-transform: uppercase;')
    }
    clusterHeader
            .addClass('part-header')
            .append($('<td style="padding-left: 0.1em;">')
                    .append('<b>')
                    .append('<span>')
                    .text(text));
    tbody.append(clusterHeader);
}

function calculateMaxRate(list, measureType) {
    const uppercaseValue = measureType.toUpperCase()
    let maxRate = 0
    list.forEach(item => {
        item.unigrams.forEach(word => {
            if (word.rateMap[uppercaseValue] > maxRate) {
                maxRate = word.rateMap[uppercaseValue]
            }
        })
    })
    return maxRate
}

function createResultTableHeader(tbody, table_num = 0) {
    let tokenTerm, lemmaTerm;

    if (langChangeButton.attr('data-lang') === 'ru') {
        tokenTerm = 'ТОКЕН';
        lemmaTerm = 'ЛЕММА';
    } else {
        tokenTerm = 'TOKEN';
        lemmaTerm = 'LEMMA';
    }

    const toggle_id = 'tableLemmaToggle' + `${table_num+1}`;

    const row = $('<tr>');
    const col = $('<td style="padding-left: 0.2em;padding-right: 0.2em;">');
    row.append(col);
    tbody.append(row);
    const toggleBox = $('<div></div>').addClass('toggle-box');
    const toggleWordForm = $('<a></a>').addClass('toggle-wordform').text(`${tokenTerm}`);
    toggleBox.append(toggleWordForm);
    const label = $('<label></label>').addClass('switch');
    toggleBox.append(label);
    const input = $('<input type="checkbox">');
    const slider = $('<span></span>').addClass('slider round').attr('id', `${toggle_id}`);

    // add click function to slider
    slider.click(function ()  {
        tokenLemmaSwitch(table_num);
    })

    label.append(input, slider);
    const toggleLemma = $('<a></a>').addClass('toggle-lemma').text(`${lemmaTerm}`);
    toggleBox.append(toggleLemma);

    col.append(toggleBox);
    lemmaTokenSwitchLemmaEnabledForResultTable[table_num] = false;
}

function tokenLemmaSwitch(table_num) {
    lemmaTokenSwitchLemmaEnabledForResultTable[table_num] = !lemmaTokenSwitchLemmaEnabledForResultTable[table_num];
    drawTableResults(table_num)
}

function adjustTable(unigram_place, table) {
    const filter1 = document.getElementById('search-filter1');
    const filter2 = document.getElementById('search-filter2');
    const filter3 = document.getElementById('search-filter3');
    const filter4 = document.getElementById('search-filter4');

    let leftEdge;
    let rightEdge;

    function setEdges(filter) {
        leftEdge = filter.getBoundingClientRect().left + window.scrollX;
        rightEdge = filter.getBoundingClientRect().right + window.scrollX;
    }

    if (unigram_place === 1) {
        setEdges(filter1);
    } else if (unigram_place === 2) {
        setEdges(filter2);
    } else if (unigram_place === 3){
        setEdges(filter3);
    } else {
        setEdges(filter4);
    }

    table.style.position = 'sticky';
    table.style.left = `${leftEdge}px`;
    table.style.width = `${rightEdge - leftEdge}px`;
}

export {setCollocations, drawResults};