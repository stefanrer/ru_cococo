class WebRequest:
    def __init__(self, request):
        self.word1: str = self._get_value(request, "word1", value_type=str)
        self.part1: str = self._get_value(request, "part1", "all", value_type=str)
        self.filter1: str = self._get_value(request, "filter1", value_type=str)
        self.is_lemma1: bool = self._get_value(request, "isLemma1", value_type=bool)
        self.word2: str = self._get_value(request, "word2", value_type=str)
        self.part2: str = self._get_value(request, "part2", "all", value_type=str)
        self.filter2: str = self._get_value(request, "filter2", value_type=str)
        self.is_lemma2: bool = self._get_value(request, "isLemma2", value_type=bool)
        self.word3: str = self._get_value(request, "word3", value_type=str)
        self.part3: str = self._get_value(request, "part3", "all", value_type=str)
        self.filter3: str = self._get_value(request, "filter3", value_type=str)
        self.is_lemma3: bool = self._get_value(request, "isLemma3", value_type=bool)
        self.word4: str = self._get_value(request, "word4", value_type=str)
        self.part4: str = self._get_value(request, "part4", "all", value_type=str)
        self.filter4: str = self._get_value(request, "filter4", value_type=str)
        self.is_lemma4: bool = self._get_value(request, "isLemma4", value_type=bool)
        self.n_grams: int = self._get_value(request, "nGrams", value_type=int)
        self.advanced: bool = self._get_value(request, "advanced", value_type=bool)

    def __str__(self):
        return (
            f"Request:\n"
            f"n_grams: {self.n_grams}\n"
            f"word1: {self.word1} is Lemma: {self.is_lemma1}\n"
            f"word2: {self.word2} is Lemma: {self.is_lemma2}\n"
            f"word3: {self.word3} is Lemma: {self.is_lemma3}\n"
            f"word4: {self.word4} is Lemma: {self.is_lemma4}\n"
            f"part1: {self.part1}\n"
            f"part2: {self.part2}\n"
            f"part3: {self.part3}\n"
            f"part4: {self.part4}\n"
            f"filter1: {self.filter1}\n"
            f"filter2: {self.filter2}\n"
            f"filter3: {self.filter3}\n"
            f"filter4: {self.filter4}\n"
        )

    @staticmethod
    def _get_value(request, key, empty_value="", value_type=None):
        value = request.get(key, None)
        if value_type is not None:
            if value_type == bool:
                if value == "true":
                    value = True
                else:
                    value = False
            elif value_type == str:
                value = str(value).lower()
            else:
                value = value_type(value)
        return value if value != empty_value else None
