from collections import defaultdict
import json
import pickle
import os.path


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    if not os.path.isfile('pair_words2nfreq.pkl') or os.path.isfile('word2nfreq.pkl'):
        pair_words_freq,words2nfreq = read_pair_words(corpus)
        pickle.dump(pair_words_freq, open('pair_words2nfreq.pkl', 'wb'))
        pickle.dump(pair_words_freq, open('word2nfreq.pkl', 'wb'))

    words_combinations = pickle.load(open('pair_words2nfreq.pkl', 'rb'))
    words2nfreq = pickle.load(open('pair_words2nfreq.pkl', 'rb'))
    lst = predict_trigram(words_combinations,words2nfreq, input, candidates)

    return lst  # return your solution

def predict_trigram(words_combinations,words2nfreq, input, candidates_file):
    candidates = get_candidates(candidates_file)
    print("candidantes: ", candidates)
    probabilities = defaultdict(list)
    with open(input, 'r', encoding='utf-8') as fin:
        print('reading the input file...')
        lines_list = fin.readlines()
        for line_num, line in enumerate(lines_list):
            words_list = line.split()
            for i, word in enumerate(words_list):
                if '___' in word:
                    for candidate in candidates:
                        if (i == 0):
                            if (line_num == 0 or words_list[line_num-1][-1][-1]=='.'):  # If word is first
                                prev_word = candidate
                                word = words_list[i + 1].translate(str.maketrans("", "", '.,\n'))
                                s = prev_word + " " + word
                                probability = words_combinations[s] / words2nfreq[word]
                                probabilities[candidate].append(probability)
                                continue
                            else:  # If word is first in line but not in the document
                                prev_word = words_list[line_num-1][-1].translate(str.maketrans("", "", '.,\n'))
                        else:  # Word isn't first in line
                            prev_word = words_list[i - 1].translate(str.maketrans("", "", '.,\n'))
                        word = candidate
                        if(i == len(words_list)-1):
                            if(line_num==len(lines_list)-1):  # If word is last
                                s = prev_word + " " + word
                                probability = words_combinations[s] / words2nfreq[prev_word]
                                probabilities[candidate].append(probability)
                                continue
                            else:  # If word is last in line but not in the document
                                next_word = lines_list[line_num+1][0].translate(str.maketrans("", "", '.,\n'))
                        else:  # Word isn't last in line
                            next_word = words_list[i+1].translate(str.maketrans("", "", '.,\n'))
                        s_prev = prev_word + " " + word
                        s_next = word + " " + next_word
                        probability = (words_combinations[s_prev] / words2nfreq[prev_word])*(words_combinations[s_next] / words2nfreq[next_word])
                        probabilities[candidate].append(probability)
    save_probablities(probabilities)
    return predict_best_combination(probabilities)

def read_pair_words(filename):
    prev_word = None
    pair_words = defaultdict(int)
    words_freq = defaultdict(int)
    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        # read each line, removing commas points and newlines.
        for i, line in enumerate([i.translate(str.maketrans("", "", '.,\n')) for i in fin.readlines()]):
            for word in line.split():
                if (prev_word == None):
                    prev_word = word
                    continue
                else:
                    pair_words[prev_word + " " + word] += 1
                    words_freq[word]+=1
                    prev_word = word
            if i % 100000 == 0:
                print(i)
    return pair_words,words_freq


def get_candidates(candidates_file):
    with open(candidates_file, 'r', encoding='utf-8') as fin:
        return [i.strip('\n') for i in fin.readlines()]


def predict_bigram(words_combinations, input, candidates_file):
    candidates = get_candidates(candidates_file)
    print("candidantes: ",candidates)
    probabilities = defaultdict(list)
    total_words = sum(words_combinations.values())/2
    with open(input, 'r', encoding='utf-8') as fin:
        print('reading the input file...')
        for line_num, line in enumerate([i.translate(str.maketrans("", "", '.,\n')) for i in fin.readlines()]):
            words_list = line.split()
            for i, word in enumerate(words_list):
                if '___' in word:
                    for candidate in candidates:
                        s = words_list[i - 1] + " " + candidate
                        probability = words_combinations[s] / total_words
                        probabilities[candidate].append(probability)
    save_probablities(probabilities)
    return predict_best_combination(probabilities)


def predict_best_combination(probabilities):
    n = len(probabilities.keys())
    final = [None] * n
    adapted_probabilities = defaultdict(list)
    for candidate in probabilities.keys():
        prob_sum = sum(probabilities[candidate])
        adapted_probabilities[candidate] = [i/prob_sum for i in probabilities[candidate]]
    for _ in range(n):
        max_prob = float('-inf')
        for candidate in adapted_probabilities.keys():
            curr_max = max(adapted_probabilities[candidate])
            if(curr_max>max_prob):
                max_prob = curr_max
                candidate_max = candidate
                pos_max = adapted_probabilities[candidate].index(curr_max)
        for candidate in adapted_probabilities.keys():
            adapted_probabilities[candidate].pop(pos_max)
        adapted_probabilities.pop(candidate_max,None)
        while(final[pos_max]!=None):
            pos_max+=1
        final[pos_max] = candidate_max
    return final

def save_probablities(probablities):
    with open("probablities.json", "w") as outfile:
        outfile.write(json.dumps(probablities, indent=2))


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)

