import math
import numpy as np
from collections import defaultdict
from App.database import find_bigrams, bigram_trigram_rel, find_trigrams, find_fourgrams, PART_OF_SPEECH_ORDER
from App.database import TOTAL_BIGRAM_COUNT, create_colligation_global
from App.request import WebRequest

Colligation_Global = create_colligation_global(True)

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


def calculate_kld_internal(global_count, actual_count):
    kl_div = float(0)
    normalization_param = float(0)

    for g, a in zip(global_count, actual_count):
        if g is None or g == 0 or a is None or a == 0:
            continue

        kl_div += g * np.log(g / a)
        normalization_param += g * np.log(g)

    non_null_values = len([g for g in global_count if g is not None])

    return kl_div / (normalization_param + np.log(non_null_values))


def calculate_jsd(global_count, actual_count):
    average = [(g if g is not None else float(0) + a) / 2 for g, a in zip(global_count, actual_count)]
    jsd = (calculate_kld_internal(global_count, average) + calculate_kld_internal(actual_count, average)) / 2
    return round(jsd, 4)


def calculate_kld(global_count, actual_count):
    actual_double = [float(a) for a in actual_count]
    kld = calculate_kld_internal(global_count, actual_double)
    return round(kld, 4)


def calculate_colligations(part, result_group, index_mapping):
    # print(f"part: {part} Calculating colligations...")
    result_colligations = []
    part_global_count = []
    part_actual_count = []

    # iterate over part features
    for feature in Colligation_Global[part]:
        feature_values = []
        feature_global_count = []
        feature_actual_count = []

        # iterate over possible feature values
        for feature_value in Colligation_Global[part][feature]:
            if feature_value is None:  # skip if None
                continue
            global_count = Colligation_Global[part][feature][feature_value]
            actual_count = sum(result[index_mapping["result_unigram"]].freq for result in result_group
                               if getattr(result[index_mapping["result_morphology"]], feature) == feature_value)
            if actual_count == 0 or global_count == 0:
                # print(f"actual or global count 0: {actual_count}| {global_count}")
                continue
            feature_values.append({"feature_value": feature_value, "globalCount": global_count, "actualCount": actual_count})

            # print(f"feature: {feature}, feature_value: {feature_value}, global_count: {global_count}, actual_count: {actual_count}")

            feature_global_count.append(global_count)
            feature_actual_count.append(actual_count)

        # skip calculation if feature empty
        if len(feature_global_count) < 1 or len(feature_actual_count) < 1:
            continue

        # print(f"feature_global_count: {feature_global_count}, feature_actual_count: {feature_actual_count}")

        # Calculate the KLD
        feature_kld = calculate_kld(feature_global_count, feature_actual_count)

        # Calculate the JSD
        feature_jsd = calculate_jsd(feature_global_count, feature_actual_count)

        colligation_feature_dto = {"feature": feature, "kld": feature_kld, "jsd": feature_jsd, "feature_values": feature_values}

        #
        part_global_count.extend(feature_global_count)
        part_actual_count.extend(feature_actual_count)

        result_colligations.append(colligation_feature_dto)

    if len(part_global_count) < 1 or len(part_actual_count) < 1:
        return [], 0, 0

    part_kld = calculate_kld(part_global_count, part_actual_count)
    part_jsd = calculate_jsd(part_global_count, part_actual_count)

    return result_colligations, part_kld, part_jsd


def calculate_bigram_rates(unigram1_freq, unigram2_freq, bigram_freq):
    rate_map = {
        "TSCORE": calculate_t_score(unigram1_freq, unigram2_freq, bigram_freq),
        "DICE": calculate_mi_score(unigram1_freq, unigram2_freq, bigram_freq),
        "MI": calculate_dice_coefficient(unigram1_freq, unigram2_freq, bigram_freq),
    }
    return rate_map


def calculate_c_value(bigram):
    trigram_freq = bigram_trigram_rel(bigram)
    if len(trigram_freq) < 1:
        c_value = float(0)
    else:
        c_value = bigram.freq - (1 / float(len(trigram_freq)) * sum([trigram[0] for trigram in trigram_freq]))
    return round(c_value, 4)


def create_bigram_colligation_dto(result, index_mapping):
    bigram = result[index_mapping["bigram"]]
    input_unigram = result[index_mapping["input_unigram"]]
    result_unigram = result[index_mapping["result_unigram"]]
    result_morphology = result[index_mapping["result_morphology"]]

    colligation_dto = {
        "word": result_unigram.value,
        "lemma": result_unigram.lemma,
        "part": result_morphology.upos,
        # "rate": float(0),
        "rateMap": calculate_bigram_rates(input_unigram.freq, result_unigram.freq, bigram.freq),
        "wordFreq": result_unigram.freq,
        "ngramFreq": bigram.freq,
        "unigramId": result_unigram.id,
        "cvalue": calculate_c_value(bigram),
    }
    return colligation_dto


def get_bigram_colligation(part, result_group, index_mapping):
    colligations, part_kld, part_jsd = calculate_colligations(part, result_group, index_mapping)
    if not colligations:
        return []
    wrapper = {"part": part, "kld": part_kld, "jsd": part_jsd, "colligations": colligations}
    return wrapper


def bigram_colligation_search(colligation_request: WebRequest, limit=False):
    results = find_bigrams(colligation_request)
    index_mapping = {
        "bigram": 0,
    }
    if colligation_request.word2:
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

    # For each part, sort by ngramFreq and take the top 20 if needed
    top_unique_results_by_part = {}
    for part, result_group in unique_results_by_part.items():
        sorted_results = sorted(result_group, key=lambda x: x[index_mapping["bigram"]].freq, reverse=True)
        # top_unique_results_by_part[part] = sorted_results \
        #     if ((collocation_request.word1 and collocation_request.part2) or
        #         (collocation_request.word2 and collocation_request.part1)) \
        #     else sorted_results[:20] # only 20 results if no pos filter applied
        top_unique_results_by_part[part] = sorted_results

    colligation_dto_by_part = {}
    for part, result_group in top_unique_results_by_part.items():
        part_colligation = get_bigram_colligation(part, result_group, index_mapping)
        if part_colligation:
            colligation_dto = [create_bigram_colligation_dto(result, index_mapping) for result in result_group]
            colligation_dto_by_part[part] = (part_colligation, colligation_dto)

    colligation_dto_by_jsd = sorted(colligation_dto_by_part.items(), key=lambda x: x[1][0]["jsd"], reverse=True)

    # for part in colligation_dto_by_jsd:
    #     print(f"part: {part}")

    return [colligation_dto_by_jsd]


def trigram_colligation_search(colligation_request: WebRequest, limit=False):
    return []


def fourgram_colligation_search(colligation_request: WebRequest, limit=False):
    return []


def colligations_search(colligation_request):
    colligation_result = []
    if colligation_request.n_grams == 2:
        colligation_result = bigram_colligation_search(colligation_request)
    # elif colligation_request.n_grams == 3:
    #     print("trigram")
    #     colligation_result = trigram_colligation_search(colligation_request)
    # elif colligation_request.n_grams == 4:
    #     print("fourgram")
    #     colligation_result = fourgram_colligation_search(colligation_request)
    else:
        print("unknown operation")
    return colligation_result


