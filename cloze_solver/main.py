from collections import defaultdict
import json
from time import time
from random import shuffle

# Gets the candidates as a list from the file
def get_candidates(candidates_file):
    with open(candidates_file, 'r', encoding='utf-8') as fin:
        return fin.read().split()

# Calculate the chance accuracy by rolling 100 times.
def calculate_and_print_chance_accuracy(candidates):
    n = len(candidates)
    shuffled_candidates = candidates.copy()
    total_matching = 0
    for i in range(100):
        shuffle(shuffled_candidates)  # Shuffle the candidates order 100 times and count matching words orders
        for solution, guess in zip(candidates, shuffled_candidates):
            if solution == guess:
                total_matching += 1
    average_accuracy = total_matching / (len(candidates) * 100)  # Divide by 100 for the average and number of candidates for the percentage.
    print('Estimated chance accuracy: ',average_accuracy)

# for each missing word in the cloze gets the previous and next word.
def get_cloze_data(cloze_filename):
    prev_words = list()
    next_words = list()
    with open(cloze_filename, 'r', encoding='utf-8') as cloze_file:
        cloze = cloze_file.read().strip(',').lower().split()  # Removing commas to get the word itself.
        n = len(cloze)
        for i, word in enumerate(cloze):
            if '__' in word:
                if (i == 0 or cloze[i - 1][-1] == '.'):
                    prev_words.append(".") # Since we cant check every word that ends with '.' in the corpus because of runtime constraints, if the word ends with '.' we ignore next word chance.
                else:
                    prev_words.append(cloze[i - 1])
                if (i == n):
                    next_words.append(".")
                else:
                    next_words.append(cloze[i + 1].replace('.', ''))
    return prev_words, next_words

# Gets the frequencies of the relevant words and pair words.
def get_data_from_the_corpus(corpus, candidates):
    print("reading data from corpus...")
    with open(corpus, 'r', encoding='utf-8') as corpus_file:
        previous = "."  # we'll mark '.' as </s>
        words_dict = defaultdict(int)
        corpus_lines = corpus_file.readlines()
        for i, line in enumerate(corpus_lines):
            for word in line.strip(',').lower().split():  # ignoring commas
                stripped_word = word.strip('.')
                if stripped_word in candidates:
                    words_dict[stripped_word] += 1
                    if previous == '.' or previous in candidates:
                        words_dict[previous + " " + stripped_word] += 1
                if word[-1] == '.':
                    previous = '.'  # if last word ended with '.' we'll mark it as a new sentence instead of saving last word
                    words_dict['.'] += 1
                else:
                    previous = stripped_word
            # Uncomment to print progress:
            #if i % 100000 == 0:    print(i)
        return words_dict

#  calculates the probabilities of each candidate to each position, using the words_freq which contains relevant words and words pairs frequaecies
def calculate_probabilities(words_freq, candidate_list, prev_words,next_words):
    probablities = defaultdict(list)
    for candidate in candidate_list:
        for prev,next in zip(prev_words,next_words):
            prev_chance = 0 if words_freq[prev+" "+candidate]==0 else words_freq[prev+" "+candidate]/words_freq[prev]  # P("{prev} {word}")/P({word}) = P(word|prev)
            next_chance = 0 if words_freq[candidate+" "+next]==0 else words_freq[candidate+" "+next]/words_freq[next]  # P("{word} {next}")/P({next}) = P(word|next)
            if next =='.':
                next_chance=1  # Since we cant check every word that ends with '.' because of runtime constraints, if the word ends with '.' we ignore next word chance.
            probablities[candidate].append(prev_chance*next_chance)
    return probablities


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    t1 = time()
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    candidate_list = get_candidates(candidates)
    calculate_and_print_chance_accuracy(candidate_list)
    prev_words, next_words = get_cloze_data(input)
    words_freq = get_data_from_the_corpus(corpus,prev_words+next_words+candidate_list)
    probabilities = calculate_probabilities(words_freq, candidate_list, prev_words,next_words)
    #  Uncomment to create a file with the probabilities, to see them.
    #save_probabilities(probabilities, "probabilities.json")

    lst = predict_best_combination(probabilities)

    t2 = time()
    # Uncomment to print time took:
    #print("time took: ", (t2 - t1) / 60, "minutes")

    return lst  # return your solution

# makes probabilities proportional to their other probabilities, ex: [0,0.1,0.3] -> [0,0.25,0.75]
def calculate_adapted_probabilities(probabilities):
    adapted_probabilities = defaultdict(list)
    for candidate in probabilities.keys():
        prob_sum = sum(probabilities[candidate])
        if (prob_sum != 0):  # to avoid dividing by 0
            adapted_probabilities[candidate] = [i / prob_sum for i in probabilities[candidate]]
        else:
            adapted_probabilities[candidate] = [0 for i in probabilities[candidate]]
    return adapted_probabilities
def predict_best_combination(probabilities):
    n = len(probabilities.keys())
    final = [None] * n
    taken_positions = list()
    adapted_probabilities = calculate_adapted_probabilities(probabilities)
    #  Uncomment to create a file with the adapted probabilities, to see them.
    #save_probablities(adapted_probabilities,'proportionate_probabilities.json')
    for _ in range(n):
        max_prob = float('-inf')
        for candidate in adapted_probabilities.keys():
            curr_max = max(adapted_probabilities[candidate])  # Get the maximum probability of the candidate
            if (curr_max > max_prob):  # We search for max probability from all candidates, and insert it first in the position it had that probability
                max_prob = curr_max
                candidate_max = candidate
                pos_max = adapted_probabilities[candidate].index(curr_max)
        adapted_probabilities.pop(candidate_max, None)  # Removing the word chosen from the probabilities dict so it will only be chosen once.
        for candidate in adapted_probabilities.keys():
            adapted_probabilities[candidate].pop(pos_max)  # Removing all the taken position probabilities from the other words.
        for i in taken_positions:
            if(pos_max>=i):
                pos_max+=1  # Since we remove words already added to the list, we need to add to the index the revalent number
        taken_positions.append(pos_max)
        taken_positions.sort()
        final[pos_max] = candidate_max
        adapted_probabilities = calculate_adapted_probabilities(adapted_probabilities)  # After removing the taked positions we have to recalculate the probabilities for each word left.
    return final


def save_probabilities(probabilities, filename):
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(probabilities, indent=2))


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
