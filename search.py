import math
import os

from searchdata import get_idf, get_tf_idf, get_page_rank, get_title


def get_url_list():
    list = []
    with open(os.path.join(os.getcwd(), 'crawl_data', 'url_map.txt'), 'r') as file:
        for line in file:
            list.append(line.strip('\n').split(',')[0])
    return list


def return_top10(cosines):
    cosines = sorted(cosines.items(), reverse=True)
    clist = []
    for entry in cosines:
        for cosine in entry[1]:
            dict = {}
            dict['url'] = cosine
            dict['title'] = get_title(cosine)
            dict['score'] = entry[0]

            clist.append(dict)

    final_list = []
    index = 0
    for url in clist:

        if index >= 10:
            return final_list
        final_list.append(url)
        index += 1
    return final_list


def search(phrase, boost):
    url_list = get_url_list()

    phrase_list = phrase.lower().split(' ')

    # get word frequency
    word_frequency = {}
    for word in phrase_list:
        if word not in word_frequency:
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1

    cosines = {}
    qqueryVector = []

    sumq = 0
    for word in word_frequency:
        tf = word_frequency[word] / len(phrase_list)
        idf = get_idf(str(word))
        tf_idf = math.log2(1 + tf) * idf

        qqueryVector.append(tf_idf)
        sumq += tf_idf ** 2

    sumq = math.sqrt(sumq)

    for url in url_list:
        dqueryVector = []

        sumd = 0
        for word in word_frequency:
            tf_idf = get_tf_idf(url, word)
            dqueryVector.append(tf_idf)
            sumd += tf_idf ** 2
        sumd = math.sqrt(sumd)

        numerator = 0
        denominator = sumq * sumd
        for i in range(len(dqueryVector)):
            numerator += qqueryVector[i] * dqueryVector[i]

        if denominator == 0.0:
            if denominator in cosines:
                cosines[denominator].append(url)
            else:
                cosines[denominator] = []
                cosines[denominator].append(url)

        elif boost:
            pagerank = get_page_rank(url)
            if (numerator / denominator) * pagerank in cosines:
                cosines[(numerator / denominator) * pagerank].append(url)
            else:
                cosines[(numerator / denominator) * pagerank] = []
                cosines[(numerator / denominator) * pagerank].append(url)

        else:
            if (numerator / denominator) in cosines:
                cosines[(numerator / denominator)].append(url)
            else:
                cosines[(numerator / denominator)] = []
                cosines[(numerator / denominator)].append(url)

    return return_top10(cosines)


with open('search-results.txt', 'w') as file:
    results = search(input('Enter phrase: '), input('Boost "True" or "False": '))
    file.write(str(results))
