import csv
import re
import math
from collections import Counter

def cb(qus):
    WORD = re.compile(r'\w+')

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    vector1 = text_to_vector(qus.lower())

    datas = []
    with open('dialogs.csv', mode='r') as file:
        csvFile = csv.reader(file)
        datas = list(csvFile)[1:]  # Skip the header row

    res = []
    for d in datas:
        vector2 = text_to_vector(str(d[0].lower()))  # Assuming the question is in the first column
        cosine = get_cosine(vector1, vector2)
        res.append(cosine)

    ss = 0
    cnt = -1
    i = 0
    for s in res:
        if s > 0.3:
            if ss <= float(s):
                cnt = i
                ss = s
        i += 1

    return datas[cnt][1] if cnt != -1 else "Sorry, I don't understand."

print(cb("list of cources"))
