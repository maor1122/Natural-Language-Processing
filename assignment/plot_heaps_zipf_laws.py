import json
import pickle
import os.path
from collections import defaultdict
from matplotlib import pyplot as plt
from math import log
import seaborn as sn
from nltk.stem import WordNetLemmatizer
import nltk

sn.set()


def read_data(filename):
    word2freq = defaultdict(int)
    with open(filename, 'r',encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                word2freq[word] += 1
            if i % 100000 == 0:
                print(i)

    total_words = sum(word2freq.values())
    word2nfreq = {w: word2freq[w]/total_words for w in word2freq}
    return word2nfreq


def plot_zipf_law(word2nfreq):
    y = sorted(word2nfreq.values(), reverse=True)
    x = list(range(1, len(y)+1))

    product = [a * b for a, b in zip(x, y)]
    print(product[:1000])  # todo: print and note the roughly constant value

    y = [log(e, 2) for e in y]
    x = [log(e, 2) for e in x]

    plt.plot(x, y)
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title("Zipf's law")
    plt.show()

def read_data2(filename):
    typesNTokens = defaultdict(int)
    types = defaultdict(int)
    totalToken = 0
    totalTypes = 0
    lemmatizer = WordNetLemmatizer()
    with open(filename, 'r',encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                simple_word = lemmatizer.lemmatize(word)
                if types[simple_word]<1:
                    totalTypes+=1
                totalToken+=1
                types[simple_word]+=1
            if i % 100000 == 0:
                print(i)
            typesNTokens[totalToken] = totalTypes
    return typesNTokens

def plot_heaps_law(typesNTokens):
    x = typesNTokens.keys()
    y = typesNTokens.values()
    print(f'types: {list(y)[-1]}')
    print(f'tokens: {list(x)[-1]}')
    plt.plot(x, y)
    plt.xlabel('Tokens')
    plt.ylabel('Types')
    plt.title("Heaps' law")
    plt.show()


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    if not os.path.isfile('word2nfreq.pkl'):
        data = read_data(config['corpus'])
        pickle.dump(data, open('word2nfreq.pkl', 'wb'))

    plot_zipf_law(pickle.load(open('word2nfreq.pkl', 'rb')))

    if not os.path.isfile('typesNTokens.pkl'):
        data = read_data2(config['corpus'])
        pickle.dump(data, open('typesNTokens.pkl', 'wb'))

    plot_heaps_law(pickle.load(open('typesNTokens.pkl', 'rb')))


