const GenderFeature = {
    name:   'gender',
    title:  'род',
    values: [{value: 'masc', title: 'мужской'}, {value: 'fem', title: 'женский'}, {value: 'neut', title: 'средний'}]
};

const NumberFeature = {
    name:   'number',
    title:  'число',
    values: [{value: 'sing', title: 'единственное'}, {value: 'plur', title: 'множественное'}]
};

const AnimacyFeature = {
    name: 'animacy',
    title: 'одушевленность',
    values: [{value: 'anim', title: 'одушевленное'}, {value: 'inan', title: 'неодушевленное'}]
};

const CaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'},
        {value: 'par', title: 'разделительный'}, {value: 'voc', title: 'звательный'}
    ]
};

const nounCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'},
        {value: 'par', title: 'разделительный'}
    ]
};


const verbCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'}
    ]
};

const adjCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'}
    ]
};

const pronCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'}
    ]
};

const adpCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'}
    ]
};

const numCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'}
    ]
};

const propnCaseFeature = {
    name:   'case',
    title:  'падеж',
    values: [
        {value: 'nom', title: 'именительный'}, {value: 'gen', title: 'родительный'}, {value: 'dat', title: 'дательный'},
        {value: 'acc', title: 'винительный'}, {value: 'ins', title: 'творительный'}, {value: 'loc', title: 'предложный'},
        {value: 'voc', title: 'звательный'}
    ]
};

const VerbFormFeature = {
    name: 'verbform',
    title: 'форма глагола',
    values: [{value: 'conv', title: 'деепричастие'}, {value: 'fin', title: 'личная форма'}, {value: 'inf', title: 'инфинитив'},
    {value: 'part', title: 'причастие'}]
};

const auxVerbFormFeature = {
    name: 'verbform',
    title: 'форма глагола',
    values: [{value: 'conv', title: 'деепричастие'}, {value: 'fin', title: 'личная форма'}, {value: 'inf', title: 'инфинитив'}]
};

const MoodFeature = {
    name: 'mood',
    title: 'наклонение',
    values: [{value: 'ind', title: 'изъявительное'}, {value: 'cnd', title: 'условное'}, {value: 'imp', title: 'повелительное'}]
};

const verbMoodFeature = {
    name: 'mood',
    title: 'наклонение',
    values: [{value: 'ind', title: 'изъявительное'}, {value: 'imp', title: 'повелительное'}]
};

const partMoodFeature = {
    name: 'mood',
    title: 'наклонение',
    values: [{value: 'cnd', title: 'условное'}]
};

const sconjMoodFeature = {
    name: 'mood',
    title: 'наклонение',
    values: [{value: 'cnd', title: 'условное'}]
};

const auxMoodFeature = {
    name: 'mood',
    title: 'наклонение',
    values: [{value: 'ind', title: 'изъявительное'}, {value: 'imp', title: 'повелительное'}]
};

const TenseFeature = {
    name:   'tense',
    title:  'время',
    values: [{value: 'pres', title: 'настоящее'}, {value: 'past', title: 'прошедшее'}, {value: 'fut', title: 'будущее'}]
};

const auxTenseFeature = {
    name:   'tense',
    title:  'время',
    values: [{value: 'pres', title: 'настоящее'}, {value: 'past', title: 'прошедшее'}]
};

const AspectFeature = {
    name:   'aspect',
    title:  'вид',
    values: [{value: 'perf', title: 'совершенный'}, {value: 'imp', title: 'несовершенный'}]
};

const VoiceFeature = {
    name: 'voice',
    title: 'залог',
    values: [{value: 'act', title: 'действительный'}, {value: 'pass', title: 'страдательный'}, {value: 'mid', title: 'возвратный'}]
};

const PersonFeature = {
    name: 'person',
    title: 'лицо',
    values: [{value: '1', title: 'первое'}, {value: '2', title: 'второе'}, {value: '3', title: 'третье'}]
};

const DegreeFeature = {
    name: 'degree',
    title: 'степень',
    values: [{value: 'pos', title: 'положительная'}, {value: 'cmp', title: 'сравнительная'}, {value: 'sup', title: 'превосходная'}]
};

const PolarityFeature = {
    name: 'polarity',
    title: 'полярность',
    values: [{value: 'pos', title: 'положительная'}, {value: 'neg', title: 'отрицательная'}]
};

const advPolarityFeature = {
    name: 'polarity',
    title: 'полярность',
    values: [{value: 'neg', title: 'отрицательная'}]
};

const partPolarityFeature = {
    name: 'polarity',
    title: 'полярность',
    values: [{value: 'neg', title: 'отрицательная'}]
};

// Feature to part relation
const nounFeatures = [
    GenderFeature,
    NumberFeature,
    AnimacyFeature,
    nounCaseFeature
];

const verbFeatures = [
    GenderFeature,
    AnimacyFeature,
    NumberFeature,
    verbCaseFeature,
    VerbFormFeature,
    verbMoodFeature,
    TenseFeature,
    AspectFeature,
    VoiceFeature,
    PersonFeature,
];

const adjFeatures = [
    GenderFeature,
    NumberFeature,
    adjCaseFeature,
    DegreeFeature,
];

const advFeatures = [
    DegreeFeature,
    advPolarityFeature,
];

const partFeatures = [
    MoodFeature,
    partPolarityFeature
];

const pronFeatures = [
    GenderFeature,
    AnimacyFeature,
    NumberFeature,
    pronCaseFeature,
    PersonFeature
];

const adpFeatures = [
    GenderFeature,
    AnimacyFeature,
    adpCaseFeature,
];

const numFeatures = [
    GenderFeature,
    AnimacyFeature,
    numCaseFeature,
];

const propnFeatures = [
    GenderFeature,
    AnimacyFeature,
    NumberFeature,
    propnCaseFeature,

];

const sconjFeatures = [
    sconjMoodFeature,
];

const auxFeatures = [
    GenderFeature,
    NumberFeature,
    auxVerbFormFeature,
    auxMoodFeature,
    auxTenseFeature,
    PersonFeature
];

const features = {
    noun: nounFeatures,
    verb: verbFeatures,
    adj:  adjFeatures,
    adv: advFeatures,
    part: partFeatures,
    pron: pronFeatures,
    adp: adpFeatures,
    num: numFeatures,
    propn: propnFeatures,
    sconj: sconjFeatures,
    aux: auxFeatures,
};

const allFeatures = [
    ...features.noun,
    ...features.verb,
    ...features.adj,
    ...features.adv,
    ...features.pron,
    ...features.adp,
    ...features.num,
    ...features.propn,
    ...features.sconj,
    ...features.aux,
];

export { allFeatures, features};