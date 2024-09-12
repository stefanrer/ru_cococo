from sqlalchemy import create_engine, MetaData, Table, String, Column, Integer, ForeignKey, func, select, or_, and_
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, sessionmaker, relationship, aliased
from collections import defaultdict
from App.request import WebRequest

PART_OF_SPEECH_ORDER = {
    "noun": 1,
    "adj": 5,
    "num": 10,
    "pron": 15,
    "verb": 20,
    "adv": 25,
    "adp": 30,
    "cconj": 35,
    "sconj": 40,
    "part": 45,
    "intj": 50,
    # propn TODO: сделать грам. парам. внутри существительного
    # aux  TODO: Просто глагол
}


connection_string = "mysql+mysqlconnector://root:12345678@db:3307/ru_cococo"
engine = create_engine(connection_string, echo=False)
base = declarative_base()


class Morphology(base):
    __tablename__ = 'morphology'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    upos: Mapped[str] = mapped_column(String(64))
    foreign: Mapped[str] = mapped_column(String(64))
    gender: Mapped[str] = mapped_column(String(64))
    animacy: Mapped[str] = mapped_column(String(64))
    number: Mapped[str] = mapped_column(String(64))
    case: Mapped[str] = mapped_column(String(64))
    degree: Mapped[str] = mapped_column(String(64))
    verbform: Mapped[str] = mapped_column(String(64))
    mood: Mapped[str] = mapped_column(String(64))
    tense: Mapped[str] = mapped_column(String(64))
    aspect: Mapped[str] = mapped_column(String(64))
    voice: Mapped[str] = mapped_column(String(64))
    polarity: Mapped[str] = mapped_column(String(64))
    person: Mapped[str] = mapped_column(String(64))
    variant: Mapped[str] = mapped_column(String(64))


# class ColligationGlobal(base):
#     __tablename__ = 'colligationglobal'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     upos: Mapped[str] = mapped_column(String(64))
#     feature_name: Mapped[str] = mapped_column(String(64))
#     feature_value: Mapped[str] = mapped_column(String(64), nullable=True)
#     frequency: Mapped[int] = mapped_column(Integer)


class Unigram(base):
    __tablename__ = 'unigram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    freq: Mapped[int] = mapped_column(default=1)
    lemma: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[str] = mapped_column(String(64), nullable=False)
    morphology_id: Mapped[int] = mapped_column(ForeignKey(Morphology.id), nullable=False)

    morphology = relationship('Morphology', foreign_keys='Unigram.morphology_id')


class Bigram(base):
    __tablename__ = 'bigram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    freq: Mapped[int] = mapped_column(default=1)
    first_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    second_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)

    first_unigram = relationship('Unigram', foreign_keys='Bigram.first_unigram_id')
    second_unigram = relationship('Unigram', foreign_keys='Bigram.second_unigram_id')


class Trigram(base):
    __tablename__ = 'trigram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    freq: Mapped[int] = mapped_column(default=1)
    first_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    second_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    third_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)

    first_unigram = relationship('Unigram', foreign_keys='Trigram.first_unigram_id')
    second_unigram = relationship('Unigram', foreign_keys='Trigram.second_unigram_id')
    third_unigram = relationship('Unigram', foreign_keys='Trigram.third_unigram_id')


class Fourgram(base):
    __tablename__ = 'fourgram'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    freq: Mapped[int] = mapped_column(default=1)
    first_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    second_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    third_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)
    fourth_unigram_id: Mapped[int] = mapped_column(ForeignKey(Unigram.id), nullable=False)

    first_unigram = relationship('Unigram', foreign_keys='Fourgram.first_unigram_id')
    second_unigram = relationship('Unigram', foreign_keys='Fourgram.second_unigram_id')
    third_unigram = relationship('Unigram', foreign_keys='Fourgram.third_unigram_id')
    fourth_unigram = relationship('Unigram', foreign_keys='Fourgram.fourth_unigram_id')


class Colligationglobal(base):
    __tablename__ = 'colligationglobal'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    upos: Mapped[str] = mapped_column(String(64), nullable=False)
    feature_name: Mapped[str] = mapped_column(String(64), nullable=False)
    feature_value: Mapped[str] = mapped_column(String(64))
    freq: Mapped[int] = mapped_column(nullable=False)


base.metadata.create_all(engine)
factory = sessionmaker(bind=engine)
session = factory()
metadata = MetaData()

TOTAL_BIGRAM_COUNT = session.query(func.sum(Bigram.freq)).scalar()

# UPOS_VALUES = session.query(Morphology.upos).distinct().all()

Unigram1 = aliased(Unigram)
Unigram2 = aliased(Unigram)
Unigram3 = aliased(Unigram)
Unigram4 = aliased(Unigram)

Bigram1 = aliased(Bigram)
Bigram2 = aliased(Bigram)
Bigram3 = aliased(Bigram)

Trigram1 = aliased(Trigram)
Trigram2 = aliased(Trigram)

Morphology1 = aliased(Morphology)
Morphology2 = aliased(Morphology)
Morphology3 = aliased(Morphology)
Morphology4 = aliased(Morphology)


def get_selection(operation):
    selection_dict = {
        "bigram": [
            Bigram,
            Unigram1, Unigram2,
            Morphology1, Morphology2
        ],
        "trigram": [
            Trigram,
            Bigram1.freq, Bigram2.freq,
            Unigram1, Unigram2, Unigram3,
            Morphology1, Morphology2, Morphology3
        ],
        "fourgram": [
            Fourgram,
            Trigram1.freq, Trigram2.freq,
            Bigram1.freq, Bigram2.freq, Bigram3.freq,
            Unigram1, Unigram2, Unigram3, Unigram4,
            Morphology1, Morphology2, Morphology3, Morphology4
        ]
    }
    return selection_dict[operation]


def get_joins(operation):
    joins_dict = {
        "bigram": [
            (Unigram1, Bigram.first_unigram),
            (Unigram2, Bigram.second_unigram),
            (Morphology1, Unigram1.morphology),
            (Morphology2, Unigram2.morphology),
        ],
        "trigram": [
            (Unigram1, Trigram.first_unigram_id == Unigram1.id),
            (Unigram2, Trigram.second_unigram_id == Unigram2.id),
            (Unigram3, Trigram.third_unigram_id == Unigram3.id),
            (Bigram1, and_(Trigram.first_unigram_id == Bigram1.first_unigram_id, Trigram.second_unigram_id == Bigram1.second_unigram_id)),
            (Bigram2, and_(Trigram.second_unigram_id == Bigram2.first_unigram_id, Trigram.third_unigram_id == Bigram2.second_unigram_id)),
            (Morphology1, Unigram1.morphology_id == Morphology1.id),
            (Morphology2, Unigram2.morphology_id == Morphology2.id),
            (Morphology3, Unigram3.morphology_id == Morphology3.id),
        ],
        "fourgram": [
            (Unigram1, Fourgram.first_unigram_id == Unigram1.id),
            (Unigram2, Fourgram.second_unigram_id == Unigram2.id),
            (Unigram3, Fourgram.third_unigram_id == Unigram3.id),
            (Unigram4, Fourgram.fourth_unigram_id == Unigram4.id),
            (Bigram1, and_(Fourgram.first_unigram_id == Bigram1.first_unigram_id,
                           Fourgram.second_unigram_id == Bigram1.second_unigram_id)),
            (Bigram2, and_(Fourgram.second_unigram_id == Bigram2.first_unigram_id,
                           Fourgram.third_unigram_id == Bigram2.second_unigram_id)),
            (Bigram3, and_(Fourgram.third_unigram_id == Bigram3.first_unigram_id,
                           Fourgram.fourth_unigram_id == Bigram3.second_unigram_id)),
            (Trigram1, and_(Fourgram.first_unigram_id == Trigram1.first_unigram_id,
                            Fourgram.second_unigram_id == Trigram1.second_unigram_id,
                            Fourgram.third_unigram_id == Trigram1.third_unigram_id)),
            (Trigram2, and_(Fourgram.second_unigram_id == Trigram2.first_unigram_id,
                            Fourgram.third_unigram_id == Trigram2.second_unigram_id,
                            Fourgram.fourth_unigram_id == Trigram2.third_unigram_id)),
            (Morphology1, Unigram1.morphology_id == Morphology1.id),
            (Morphology2, Unigram2.morphology_id == Morphology2.id),
            (Morphology3, Unigram3.morphology_id == Morphology3.id),
            (Morphology4, Unigram4.morphology_id == Morphology4.id),
        ],
    }
    return joins_dict[operation]


def get_search_conditions(request: WebRequest):
    condition_dict = {
        "word1": lambda value: Unigram1.value == value if not request.is_lemma1
        else Unigram1.lemma == value,  # Lemma/Token switch
        "word2": lambda value: Unigram2.value == value if not request.is_lemma2
        else Unigram2.lemma == value,  # Lemma/Token switch
        "word3": lambda value: Unigram3.value == value if not request.is_lemma3
        else Unigram3.lemma == value,  # Lemma/Token switch
        "word4": lambda value: Unigram4.value == value if not request.is_lemma4
        else Unigram4.lemma == value,  # Lemma/Token switch
        "part1": lambda value: Morphology1.upos == value,
        "part2": lambda value: Morphology2.upos == value,
        "part3": lambda value: Morphology3.upos == value,
        "part4": lambda value: Morphology4.upos == value,
        "filters1": {
            "foreign": lambda values: or_(*[Morphology1.foreign == value for value in values]),
            "gender": lambda values: or_(*[Morphology1.gender == value for value in values]),
            "animacy": lambda values: or_(*[Morphology1.animacy == value for value in values]),
            "number": lambda values: or_(*[Morphology1.number == value for value in values]),
            "case": lambda values: or_(*[Morphology1.case == value for value in values]),
            "verbform": lambda values: or_(*[Morphology1.verbform == value for value in values]),
            "mood": lambda values: or_(*[Morphology1.mood == value for value in values]),
            "tense": lambda values: or_(*[Morphology1.tense == value for value in values]),
            "aspect": lambda values: or_(*[Morphology1.aspect == value for value in values]),
            "voice": lambda values: or_(*[Morphology1.voice == value for value in values]),
            "polarity": lambda values: or_(*[Morphology1.polarity == value for value in values]),
            "person": lambda values: or_(*[Morphology1.person == value for value in values]),
            "variant": lambda values: or_(*[Morphology1.variant == value for value in values]),
        },
        "filters2": {
            "foreign": lambda values: or_(*[Morphology2.foreign == value for value in values]),
            "gender": lambda values: or_(*[Morphology2.gender == value for value in values]),
            "animacy": lambda values: or_(*[Morphology2.animacy == value for value in values]),
            "number": lambda values: or_(*[Morphology2.number == value for value in values]),
            "case": lambda values: or_(*[Morphology2.case == value for value in values]),
            "verbform": lambda values: or_(*[Morphology2.verbform == value for value in values]),
            "mood": lambda values: or_(*[Morphology2.mood == value for value in values]),
            "tense": lambda values: or_(*[Morphology2.tense == value for value in values]),
            "aspect": lambda values: or_(*[Morphology2.aspect == value for value in values]),
            "voice": lambda values: or_(*[Morphology2.voice == value for value in values]),
            "polarity": lambda values: or_(*[Morphology2.polarity == value for value in values]),
            "person": lambda values: or_(*[Morphology2.person == value for value in values]),
            "variant": lambda values: or_(*[Morphology2.variant == value for value in values]),
        },
        "filters3": {
            "foreign": lambda values: or_(*[Morphology3.foreign == value for value in values]),
            "gender": lambda values: or_(*[Morphology3.gender == value for value in values]),
            "animacy": lambda values: or_(*[Morphology3.animacy == value for value in values]),
            "number": lambda values: or_(*[Morphology3.number == value for value in values]),
            "case": lambda values: or_(*[Morphology3.case == value for value in values]),
            "verbform": lambda values: or_(*[Morphology3.verbform == value for value in values]),
            "mood": lambda values: or_(*[Morphology3.mood == value for value in values]),
            "tense": lambda values: or_(*[Morphology3.tense == value for value in values]),
            "aspect": lambda values: or_(*[Morphology3.aspect == value for value in values]),
            "voice": lambda values: or_(*[Morphology3.voice == value for value in values]),
            "polarity": lambda values: or_(*[Morphology3.polarity == value for value in values]),
            "person": lambda values: or_(*[Morphology3.person == value for value in values]),
            "variant": lambda values: or_(*[Morphology3.variant == value for value in values]),
        },
        "filters4": {
            "foreign": lambda values: or_(*[Morphology4.foreign == value for value in values]),
            "gender": lambda values: or_(*[Morphology4.gender == value for value in values]),
            "animacy": lambda values: or_(*[Morphology4.animacy == value for value in values]),
            "number": lambda values: or_(*[Morphology4.number == value for value in values]),
            "case": lambda values: or_(*[Morphology4.case == value for value in values]),
            "verbform": lambda values: or_(*[Morphology4.verbform == value for value in values]),
            "mood": lambda values: or_(*[Morphology4.mood == value for value in values]),
            "tense": lambda values: or_(*[Morphology4.tense == value for value in values]),
            "aspect": lambda values: or_(*[Morphology4.aspect == value for value in values]),
            "voice": lambda values: or_(*[Morphology4.voice == value for value in values]),
            "polarity": lambda values: or_(*[Morphology4.polarity == value for value in values]),
            "person": lambda values: or_(*[Morphology4.person == value for value in values]),
            "variant": lambda values: or_(*[Morphology4.variant == value for value in values]),
        },
    }

    conditions = []
    # Token 1
    if request.word1:
        conditions.append(condition_dict["word1"](request.word1))
    if request.part1:
        conditions.append(condition_dict["part1"](request.part1))
    if request.filter1 is not None:
        print(request.filter1)
        filters = {morph: values.split(",") for morph, values in
                   (morph_filter.split(":") for morph_filter in request.filter1.split(";") if morph_filter)}
        print(filters)
        for morph, values in filters.items():
            conditions.append(condition_dict["filters1"][morph](values))
    # Token 2
    if request.word2:
        conditions.append(condition_dict["word2"](request.word2))
    if request.part2:
        conditions.append(condition_dict["part2"](request.part2))
    if request.filter2 is not None:
        filters = {morph: values.split(",") for morph, values in
                   (morph_filter.split(":") for morph_filter in request.filter2.split(";") if morph_filter)}
        print(filters)
        for morph, values in filters.items():
            conditions.append(condition_dict["filters2"][morph](values))
    # Token 3
    if request.word3:
        conditions.append(condition_dict["word3"](request.word3))
    if request.part3:
        conditions.append(condition_dict["part3"](request.part3))
    if request.filter3 is not None:
        filters = {morph: values.split(",") for morph, values in
                   (morph_filter.split(":") for morph_filter in request.filter3.split(";") if morph_filter)}
        print(filters)
        for morph, values in filters.items():
            conditions.append(condition_dict["filters3"][morph](values))
    # Token 4
    if request.word4:
        conditions.append(condition_dict["word4"](request.word4))
    if request.part4:
        conditions.append(condition_dict["part4"](request.part4))
    if request.filter4 is not None:
        filters = {morph: values.split(",") for morph, values in
                   (morph_filter.split(":") for morph_filter in request.filter4.split(";") if morph_filter)}
        print(filters)
        for morph, values in filters.items():
            conditions.append(condition_dict["filters4"][morph](values))
    return conditions


def get_query(request: WebRequest, operation="bigram", limit=True):
    selection = get_selection(operation)
    joins = get_joins(operation)
    filters = get_search_conditions(request)
    stmt = select(*selection)  # init query

    # Add joins
    for entity, condition in joins:
        stmt = stmt.join(entity, condition)

    # Add filters
    for condition in filters:
        stmt = stmt.where(condition)

    # if limit and ((not request.word1 and request.part1) or
    #               (not request.word2 and request.part2) or
    #               (not request.word2 and request.part2)):
    #     stmt = stmt.limit(1000)
    result = session.execute(stmt).all()
    return result


def find_bigrams(request: WebRequest):
    if (request.word1 and request.word2) or (not request.word1 and not request.word2):  # if all filled return empty
        return []
    results = get_query(request, operation="bigram")
    return results


def bigram_trigram_rel(bigram: Bigram):
    stmt = select(Trigram.freq).where(and_(Trigram.first_unigram_id == bigram.first_unigram_id, Trigram.second_unigram_id == bigram.second_unigram_id))
    results = session.execute(stmt).all()
    return results


def find_trigrams(request: WebRequest):
    if request.word1 and request.word2 and request.word3:  # if all filled return empty
        print("all filled")
        return []
    elif not request.word1 and not request.word2 and not request.word3:  # if all empty return empty
        print("none")
        return []
    results = get_query(request, operation="trigram")
    # print(results)
    return results


def find_fourgrams(request: WebRequest):
    if request.word1 and request.word2 and request.word3 and request.word4:  # if all filled return empty
        print("all filled")
        return []
    elif not request.word1 and not request.word2 and not request.word3 and not request.word4:  # if all empty return empty
        print("none")
        return []
    results = get_query(request, operation="fourgram")
    # print(results)
    return results

# print("Total Bigrams: ", TOTAL_BIGRAM_COUNT)


def create_colligation_global(exist=False):
    if exist:
        colligation_global = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        stmt = select(Colligationglobal)
        results = session.execute(stmt).all()
        for result in results:
            colligation_global[result[0].upos][result[0].feature_name][result[0].feature_value] = result[0].freq
        return colligation_global
    stmt = select(Unigram, Morphology)
    stmt = stmt.join(Morphology, Unigram.morphology_id == Morphology.id)
    results = session.execute(stmt).all()

    def get_colligation_global():
        # Initialize an empty dictionary
        colligation_global = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # Iterate over the results
        for unigram, morph in results:
            for column in Morphology.__table__.columns:
                # Skip the 'id' and 'upos' columns
                if column.name != 'id' and column.name != 'upos':
                    feature_name = column.name
                    feature_value = getattr(morph, feature_name)

                    # Increment the frequency of this feature_value for this upos
                    colligation_global[morph.upos][feature_name][feature_value] += unigram.freq

        return colligation_global

    # Call the function with your results
    colligation_global = get_colligation_global()

    for upos, middle_dict in colligation_global.items():
        print(f"{upos}:")
        for feature_name, inner_dict in middle_dict.items():
            print(f"  {feature_name}:")
            for feature_value, freq in inner_dict.items():
                print(f"    {feature_value}: {freq}")

    # For each upos, feature_name, and feature_value in the 'colligation_global' dictionary
    for upos, features in colligation_global.items():
        for feature_name, feature_values in features.items():
            for feature_value, frequency in feature_values.items():
                if feature_value is not None:
                    # Create a new ColligationGlobal object
                    colligation = Colligationglobal(
                        upos=upos,
                        feature_name=feature_name,
                        feature_value=feature_value,
                        freq=frequency
                    )

                    # Add the new object to the session
                    session.add(colligation)

    # Commit the transaction
    session.commit()

    return colligation_global




