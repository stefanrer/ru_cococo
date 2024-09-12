import math
import time
from collections import defaultdict
from App.database import TOTAL_BIGRAM_COUNT
from App.database import find_bigrams, find_trigrams, find_fourgrams, PART_OF_SPEECH_ORDER
from App.request import WebRequest


def timeit(func):
    """
    Decorator for measuring function's running time.
    """

    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result

    return measure_time


# print(f"upos values: {UPOS_VALUES}")
# valid_upos_values = [upos_value[0] for upos_value in UPOS_VALUES if upos_value[0].lower() in PART_OF_SPEECH_ORDER]
# print(f"valid upos values: {valid_upos_values}")

ru_pos_translate = {
    "noun": "Существительное",
    "verb": "Глагол",
    "adj": "Прилагательное",
    "adv": "Наречие",
    "part": "Частица",
    "pron": "Местоимение",
    "adp": "Предлог",
    "num": "Числительное",
    "propn": "Имя собственное",
    "cconj": "Союз",
    "sconj": "Подчинительный союз",
    "aux": "Вспомогательный глагол"
}


def calculate_t_score(unigram1_freq, unigram2_freq, bigram_freq):
    E_xy = float(unigram1_freq + unigram2_freq) / float(TOTAL_BIGRAM_COUNT)
    t_score = (bigram_freq - E_xy) / (bigram_freq ** 0.5)
    return round(t_score, 4)


def calculate_t_score_ua(unigram1_freq, unigram2_freq, bigram_freq):
    E_xy = float(unigram1_freq * unigram2_freq) / float(TOTAL_BIGRAM_COUNT)
    t_score = (bigram_freq - E_xy) / (bigram_freq ** 0.5)
    return round(t_score, 4)


def calculate_mi_score(unigram1_freq, unigram2_freq, bigram_freq):
    # Probability of bigram
    P_xy = float(bigram_freq) / float(TOTAL_BIGRAM_COUNT)

    # Probabilities of unigrams
    P_x = float(unigram1_freq) / float(TOTAL_BIGRAM_COUNT)
    P_y = float(unigram2_freq) / float(TOTAL_BIGRAM_COUNT)

    # MI Score
    mi_score = math.log(P_xy / (P_x * P_y), 2)

    return round(mi_score, 4)


def calculate_mi_score_ua(unigram1_freq, unigram2_freq, bigram_freq):
    e11 = (float(unigram1_freq) * float(unigram2_freq)) / float(TOTAL_BIGRAM_COUNT)
    mi_score = float(math.log(float(bigram_freq) / float(e11)))
    return round(mi_score, 4)


def calculate_dice_coefficient(unigram1_freq, unigram2_freq, bigram_freq):
    # Size of intersection (i.e., bigram frequency)
    intersection_size = float(bigram_freq)

    # Sizes of the two sets (i.e., unigram frequencies)
    set1_size = float(unigram1_freq)
    set2_size = float(unigram2_freq)

    # Dice Coefficient
    dice_coefficient = float(2.0 * intersection_size) / float(set1_size + set2_size)

    return round(dice_coefficient, 4)


def calculate_bigram_rates(unigram1_freq, unigram2_freq, bigram_freq):
    rate_map = {
        "TSCORE": calculate_t_score(unigram1_freq, unigram2_freq, bigram_freq),
        # "DICE": calculate_mi_score(),
        # "MI": calculate_dice_coefficient(),
    }
    return rate_map


def calculate_trigram_rates(bigram1_freq, bigram2_freq, unigram1_freq, unigram2_freq, unigram3_freq):
    rate_map = {
        "TSCORE":
            calculate_t_score(unigram1_freq, unigram2_freq, bigram1_freq)
            + calculate_t_score(unigram2_freq, unigram3_freq, bigram2_freq),
        # "DICE": calculate_mi_score(),
        # "MI": calculate_dice_coefficient(),
    }
    return rate_map


def calculate_fourgram_rates(bigram1_freq, bigram2_freq, bigram3_freq, unigram1_freq, unigram2_freq, unigram3_freq, unigram4_freq):
    rate_map = {
        "TSCORE":
            calculate_t_score(unigram1_freq, unigram2_freq, bigram1_freq)
            + calculate_t_score(unigram2_freq, unigram3_freq, bigram2_freq)
            + calculate_t_score(unigram3_freq, unigram4_freq, bigram3_freq)
        # "DICE": calculate_mi_score(),
        # "MI": calculate_dice_coefficient(),
    }
    return rate_map


def create_bigram_collocation_dto(result, index_mapping):
    bigram = result[index_mapping["bigram"]]
    input_unigram = result[index_mapping["input_unigram"]]
    result_unigram = result[index_mapping["result_unigram"]]
    result_morphology = result[index_mapping["result_morphology"]]

    collocation_dto = {
        "word": result_unigram.value,
        "lemma": result_unigram.lemma,
        "part": result_morphology.upos,
        # "rate": float,
        "rateMap": calculate_bigram_rates(input_unigram.freq, result_unigram.freq, bigram.freq),
        "wordFreq": result_unigram.freq,
        "ngramFreq": bigram.freq,
        "unigramId": result_unigram.id,
        # "cvalue": float,
    }
    return collocation_dto


def create_trigram_collocation_dto(result, index_mapping, word: str = "word1", combine: bool = True):
    trigram = result[index_mapping["Trigram"]]
    result_unigram = result[index_mapping["result_unigram"]]
    result_morphology = result[index_mapping["result_morphology"]]
    bigram1_freq = result[index_mapping["Bigram1_freq"]]
    bigram2_freq = result[index_mapping["Bigram2_freq"]]
    unigram1 = result[index_mapping["Unigram1"]]
    unigram2 = result[index_mapping["Unigram2"]]
    unigram3 = result[index_mapping["Unigram3"]]

    if combine:
        trigram_rates = calculate_trigram_rates(bigram1_freq, bigram2_freq, unigram1.freq, unigram2.freq, unigram3.freq)
    else:
        if word == "word1":
            trigram_rates = calculate_bigram_rates(unigram1.freq, unigram2.freq, bigram1_freq)
        elif word == "word2":
            trigram_rates = calculate_trigram_rates(bigram1_freq, bigram2_freq, unigram1.freq, unigram2.freq, unigram3.freq)  # TODO: Уточнить как поступать
        else:
            trigram_rates = calculate_bigram_rates(unigram2.freq, unigram3.freq, bigram2_freq)

    collocation_dto = {
        "word": result_unigram.value,
        "lemma": result_unigram.lemma,
        "part": result_morphology.upos,
        # "rate": float,
        "rateMap": trigram_rates,
        "wordFreq": result_unigram.freq,
        "ngramFreq": trigram.freq,
        "unigramId": result_unigram.id,
        # "cvalue": float,
    }
    return collocation_dto


def create_fourgram_collocation_dto(result, index_mapping, word: str = "word1", combine: bool = True):
    fourgram = result[index_mapping["Fourgram"]]
    result_unigram = result[index_mapping["result_unigram"]]
    result_morphology = result[index_mapping["result_morphology"]]
    trigram1_freq = result[index_mapping["Trigram1_freq"]]
    trigram2_freq = result[index_mapping["Trigram2_freq"]]
    bigram1_freq = result[index_mapping["Bigram1_freq"]]
    bigram2_freq = result[index_mapping["Bigram2_freq"]]
    bigram3_freq = result[index_mapping["Bigram3_freq"]]
    unigram1 = result[index_mapping["Unigram1"]]
    unigram2 = result[index_mapping["Unigram2"]]
    unigram3 = result[index_mapping["Unigram3"]]
    unigram4 = result[index_mapping["Unigram4"]]

    if combine:
        fourgram_rates = calculate_fourgram_rates(bigram1_freq, bigram2_freq, bigram3_freq, unigram1.freq,
                                                  unigram2.freq, unigram3.freq, unigram4.freq)
    elif word == "word1":
        fourgram_rates = calculate_bigram_rates(unigram1.freq, unigram2.freq, bigram1_freq)
    elif word == "word2":
        fourgram_rates = calculate_trigram_rates(bigram1_freq, bigram2_freq, unigram1.freq, unigram2.freq, unigram3.freq)  # TODO: Уточнить как поступать
    elif word == "word3":
        fourgram_rates = calculate_trigram_rates(bigram2_freq, bigram3_freq, unigram2.freq, unigram3.freq, unigram4.freq)  # TODO: Уточнить как поступать
    else:  # word4
        fourgram_rates = calculate_bigram_rates(unigram3.freq, unigram4.freq, bigram3_freq)

    collocation_dto = {
        "word": result_unigram.value,
        "lemma": result_unigram.lemma,
        "part": result_morphology.upos,
        # "rate": float,
        "rateMap": fourgram_rates,
        "wordFreq": result_unigram.freq,
        "ngramFreq": fourgram.freq,
        "unigramId": result_unigram.id,
        # "cvalue": float,
    }
    return collocation_dto


def filter_duplicated_words(result_map):
    for part, words in result_map.items():
        # Create a dictionary where the keys are the unigrams and the values are lists of all collocations with that word
        word_dict = {}
        for collocation in words:
            if collocation["word"] not in word_dict:
                word_dict[collocation["word"]] = []
            word_dict[collocation["word"]].append(collocation)

        # For each word, keep only the collocation with the maximum ngramFreq
        filtered_list = [max(collocations, key=lambda x: x["ngramFreq"]) for collocations in word_dict.values()]

        # Update the unigrams in the result_map
        result_map[part] = filtered_list


def create_grouped_collocation_dto(part, words):
    # Sort the unigrams based on the 'TSCORE' in the 'rateMap' in descending order
    # unigrams = sorted(unigrams, key=lambda x: x['rateMap']['TSCORE'], reverse=True)
    #
    # # Retain only the top 10
    # unigrams = unigrams[:10]

    grouped_collocation = {
        "part": part,
        "pardCode": part.lower(),
        "unigrams": words,
        "order": PART_OF_SPEECH_ORDER[part.lower()],
    }
    return grouped_collocation


def fourgram_collocation_search(collocation_request: WebRequest):
    print(collocation_request)
    results = find_fourgrams(collocation_request)
    print(f"found: {len(results)} results")
    index_mapping = {
        "Fourgram": 0,
        "Trigram1_freq": 1,
        "Trigram2_freq": 2,
        "Bigram1_freq": 3,
        "Bigram2_freq": 4,
        "Bigram3_freq": 5,
        "Unigram1": 6,
        "Unigram2": 7,
        "Unigram3": 8,
        "Unigram4": 9,
        "Morphology1": 10,
        "Morphology2": 11,
        "Morphology3": 12,
        "Morphology4": 13,
    }

    result_fourgrams = []

    missing_words = []
    if not collocation_request.word1:
        missing_words.append("word1")
    if not collocation_request.word2:
        missing_words.append("word2")
    if not collocation_request.word3:
        missing_words.append("word3")
    if not collocation_request.word4:
        missing_words.append("word4")

    for word in missing_words:
        if word == "word1":  # word 1 empty
            index_mapping["result_unigram"] = 6
            index_mapping["result_morphology"] = 10
        elif word == "word2":  # word 2 empty
            index_mapping["result_unigram"] = 7
            index_mapping["result_morphology"] = 11
        elif word == "word3":  # word 3 empty
            index_mapping["result_unigram"] = 8
            index_mapping["result_morphology"] = 12
        else:  # word 4 empty
            index_mapping["result_unigram"] = 9
            index_mapping["result_morphology"] = 13

        # Group the results by part
        results_by_part = defaultdict(list)
        for result in results:
            part = result[index_mapping["result_morphology"]].upos
            if part.lower() in PART_OF_SPEECH_ORDER:
                results_by_part[part].append(result)

        # For each part, retain only unique unigrams based on max ngramFreq
        unique_results_by_part = {}
        for part, result_group in results_by_part.items():
            word_dict = {}
            for result in result_group:
                word = result[index_mapping["result_unigram"]].value
                if (word not in word_dict or result[index_mapping["Fourgram"]].freq >
                        word_dict[word][index_mapping["Fourgram"]].freq):
                    word_dict[word] = result
            unique_results_by_part[part] = list(word_dict.values())

        # For each part, sort by ngramFreq and take the top 20
        top_unique_results_by_part = {}
        for part, result_group in unique_results_by_part.items():
            sorted_results = sorted(result_group, key=lambda x: x[index_mapping["Fourgram"]].freq, reverse=True)
            # top_unique_results_by_part[part] = sorted_results \
            #     if ((word == "word1" and collocation_request.part1) or
            #         (word == "word2" and collocation_request.part2) or
            #         (word == "word3" and collocation_request.part3) or
            #         (word == "word4" and collocation_request.part4)) \
            #     else sorted_results[:20]  # only 20 results if no pos filter applied
            top_unique_results_by_part[part] = sorted_results

        # Now perform the create_fourgram_collocation_dto operation
        collocation_dto_by_part = {}
        for part, result_group in top_unique_results_by_part.items():
            collocation_dto_by_part[part] = [
                create_fourgram_collocation_dto(result, index_mapping, word, len(missing_words) == 1)
                for result in result_group
            ]

        grouped_collocation = []
        for part, words in collocation_dto_by_part.items():
            grouped_collocation.append(create_grouped_collocation_dto(part, words))

        grouped_collocation.sort(key=lambda x: x['order'])  # sort by pos order

        result_fourgrams.append(grouped_collocation)

    print(len(result_fourgrams))
    return result_fourgrams


def trigram_collocation_search(collocation_request: WebRequest):
    print(collocation_request)
    results = find_trigrams(collocation_request)
    print(f"found: {len(results)} results")
    index_mapping = {
        "Trigram": 0,
        "Bigram1_freq": 1,
        "Bigram2_freq": 2,
        "Unigram1": 3,
        "Unigram2": 4,
        "Unigram3": 5,
        "Morphology1": 6,
        "Morphology2": 7,
        "Morphology3": 8
    }

    result_trigrams = []

    missing_words = []
    if not collocation_request.word1:
        missing_words.append("word1")
    if not collocation_request.word2:
        missing_words.append("word2")
    if not collocation_request.word3:
        missing_words.append("word3")

    for word in missing_words:
        if word == "word1":  # word 1 empty
            index_mapping["result_unigram"] = 3
            index_mapping["result_morphology"] = 6
        elif word == "word2":  # word 2 empty
            index_mapping["result_unigram"] = 4
            index_mapping["result_morphology"] = 7
        else:  # word 3 empty
            index_mapping["result_unigram"] = 5
            index_mapping["result_morphology"] = 8

        # Group the results by part
        results_by_part = defaultdict(list)
        for result in results:
            part = result[index_mapping["result_morphology"]].upos
            if part.lower() in PART_OF_SPEECH_ORDER:
                results_by_part[part].append(result)

        # For each part, retain only unique unigrams based on max ngramFreq
        unique_results_by_part = {}
        for part, result_group in results_by_part.items():
            word_dict = {}
            for result in result_group:
                word = result[index_mapping["result_unigram"]].value
                if (word not in word_dict or result[index_mapping["Trigram"]].freq >
                        word_dict[word][index_mapping["Trigram"]].freq):
                    word_dict[word] = result
                unique_results_by_part[part] = list(word_dict.values())

        # For each part, sort by ngramFreq and take the top 20
        top_unique_results_by_part = {}
        for part, result_group in unique_results_by_part.items():
            sorted_results = sorted(result_group, key=lambda x: x[index_mapping["Trigram"]].freq, reverse=True)
            # top_results_by_part[part] = sorted_results \
            #     if ((word == "word1" and collocation_request.part1) or
            #         (word == "word2" and collocation_request.part2) or
            #         (word == "word3" and collocation_request.part3)) \
            #     else sorted_results[:20]  # only 20 results if no pos filter applied
            top_unique_results_by_part[part] = sorted_results

        # Now perform the create_trigram_collocation_dto operation
        collocation_dto_by_part = {}
        for part, result_group in top_unique_results_by_part.items():
            collocation_dto_by_part[part] = [
                create_trigram_collocation_dto(result, index_mapping, word, len(missing_words) == 1)
                for result in result_group
            ]

        grouped_collocation = []
        for part, words in collocation_dto_by_part.items():
            grouped_collocation.append(create_grouped_collocation_dto(part, words))

        grouped_collocation.sort(key=lambda x: x['order'])  # sort by pos order

        result_trigrams.append(grouped_collocation)

    print(len(result_trigrams))

    return result_trigrams


def bigram_collocation_search(collocation_request: WebRequest, limit=False):
    results = find_bigrams(collocation_request)
    index_mapping = {
        "bigram": 0,
    }

    if collocation_request.word2:
        index_mapping["input_unigram"] = 2
        index_mapping["result_unigram"] = 1
        index_mapping["result_morphology"] = 3
    else:
        index_mapping["input_unigram"] = 1
        index_mapping["result_unigram"] = 2
        index_mapping["result_morphology"] = 4

    # Group the results by part
    results_by_part = defaultdict(list)
    for result in results:
        part = result[index_mapping["result_morphology"]].upos
        if part.lower() in PART_OF_SPEECH_ORDER:
            results_by_part[part].append(result)

    # For each part, retain only unique unigrams based on max ngramFreq
    unique_results_by_part = {}
    for part, result_group in results_by_part.items():
        word_dict = {}
        for result in result_group:
            word = result[index_mapping["result_unigram"]].value
            if (word not in word_dict or result[index_mapping["bigram"]].freq >
                    word_dict[word][index_mapping["bigram"]].freq):
                word_dict[word] = result
        unique_results_by_part[part] = list(word_dict.values())

    # For each part, sort by ngramFreq and take the top 20
    top_unique_results_by_part = {}
    for part, result_group in unique_results_by_part.items():
        sorted_results = sorted(result_group, key=lambda x: x[index_mapping["bigram"]].freq, reverse=True)
        # top_unique_results_by_part[part] = sorted_results \
        #     if ((collocation_request.word1 and collocation_request.part2) or
        #         (collocation_request.word2 and collocation_request.part1)) \
        #     else sorted_results[:20] # only 20 results if no pos filter applied
        top_unique_results_by_part[part] = sorted_results

    # Now perform the create_bigram_collocation_dto operation
    collocation_dto_by_part = {}
    for part, result_group in top_unique_results_by_part.items():
        collocation_dto_by_part[part] = [create_bigram_collocation_dto(result, index_mapping) for result in
                                         result_group]

    grouped_collocation = []
    for part, words in collocation_dto_by_part.items():
        grouped_collocation.append(create_grouped_collocation_dto(part, words))

    grouped_collocation.sort(key=lambda x: x['order'])  # sort by pos order

    # if limit and ((not collocation_request.word1 and collocation_request.part1) or
    #               (not collocation_request.word2 and collocation_request.part2) or
    #               (not collocation_request.word2 and collocation_request.part2)):
    #     print("limit")
    #     grouped_collocation[0]["unigrams"] = grouped_collocation[0]["unigrams"][:1000]
    return [grouped_collocation]


def collocations_search(collocation_request):
    collocation_result = []
    if collocation_request.n_grams == 2:
        collocation_result = bigram_collocation_search(collocation_request)
    elif collocation_request.n_grams == 3:
        collocation_result = trigram_collocation_search(collocation_request)
    elif collocation_request.n_grams == 4:
        collocation_result = fourgram_collocation_search(collocation_request)
    else:
        print("unknown operation")
    return collocation_result
