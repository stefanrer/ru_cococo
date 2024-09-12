from Collocation.collocation import collocations_search
from Colligation.colligation import colligations_search
from App.request import WebRequest
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from Backend.debug import timeit


@timeit
def search(query):
    request = WebRequest(query)
    # print(request)
    if request.advanced:
        return colligations_search(request)
    else:
        return collocations_search(request)


if __name__ == "__main__":
    collocation_args = ImmutableMultiDict(
        [('word1', 'как'), ('part1', 'all'), ('filter1', ''), ('isLemma1', 'false'), ('word2', ''), ('part2', 'all'),
         ('filter2', ''), ('isLemma2', 'false'), ('word3', ''), ('part3', 'all'), ('filter3', ''),
         ('isLemma3', 'false'), ('word4', ''), ('part4', 'all'), ('filter4', ''), ('isLemma4', 'false'),
         ('nGrams', '2'), ('advanced', 'false')])
    collocation_results = search(collocation_args)[0]
    print(f"collocation_results parts got: {len(collocation_results)}")
    count = 0
    for result in collocation_results:
        count += len(result["unigrams"])
    print(f"results got unigrams: {count}")

    colligation_args = ImmutableMultiDict(
        [('word1', 'как'), ('part1', 'all'), ('filter1', ''), ('isLemma1', 'false'), ('word2', ''), ('part2', 'all'),
         ('filter2', ''), ('isLemma2', 'false'), ('word3', ''), ('part3', 'all'), ('filter3', ''),
         ('isLemma3', 'false'), ('word4', ''), ('part4', 'all'), ('filter4', ''), ('isLemma4', 'false'),
         ('nGrams', '2'), ('advanced', 'true')])
    colligation_results = search(colligation_args)[0]
    print(f"colligation_results parts got: {len(colligation_results)}")
    print(colligation_results)

