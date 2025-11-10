import json
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression as LogReg
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


def best_features(vectorizer, vectors, labels, k=15):
    features = np.array(vectorizer.get_feature_names_out())
    # Creating the selector and selecting best K features (words)
    selector = SelectKBest(k=k)
    selector.fit(vectors, labels)
    # Getting which features were selected
    is_best = selector.get_support()
    return features[is_best]


def extract_features(source):
    # If the review is verified we include it else we skip
    if source['verified']:
        return review_content(source), source['overall']
    return None, None


def read_file(file):
    data_list, labels_list = [], []
    with open(file, 'r') as fp:
        for line in fp:
            # Extracting the reviews from the file
            review = json.loads(line)
            # Extracting the data and labels from each review
            data, label = extract_features(review)
            if label is not None:
                data_list.append(data)
                labels_list.append(label)
    return data_list, labels_list


def review_content(review):
    content = ''
    # Adding the review summary,reviewTest, unixReviewTime and reviewerName to one string
    if 'summary' in review:
        content += str(review['summary']) + '. '
    if 'reviewText' in review:
        content += str(review['reviewText']) + '. '
    if 'unixReviewTime' in review:
        content += str(review['unixReviewTime']) + '. '
    if 'reviewerName' in review:
        content += str(review['reviewerName']) + '. '
    return content


def classify(train_file, test_file):
    print(f'starting feature extraction and classification, train data: {train_file} and test: {test_file}')

    # Reading the reviews
    train_data, train_labels = read_file(train_file)
    #test_data, test_labels = read_file(test_file)

    # Converting the text of the data into numerical feature vectors
    vectorizer = CountVectorizer(ngram_range=(1, 1), max_features=999)
    train_vectors = vectorizer.fit_transform(train_data)
    #test_vectors = vectorizer.transform(test_data)

    # Using the transformer on the numerical features
    #transformer = TfidfTransformer()
    #train_vectors = transformer.fit_transform(train_vectors)
    #test_vectors = transformer.transform(test_vectors)

    # Creating and Training the classifier on the training samples.
    #classifier = LogReg(max_iter=999)
    #classifier.fit(train_vectors, train_labels)

    # Getting the classifier predictions on the test samples.
    #prediction = classifier.predict(test_vectors)

    # test_results = {'class_1_F1': f1_score(test_labels, prediction, labels=[1], average='micro'),
    #                 'class_2_F1': f1_score(test_labels, prediction, labels=[2], average='micro'),
    #                 'class_3_F1': f1_score(test_labels, prediction, labels=[3], average='micro'),
    #                 'class_4_F1': f1_score(test_labels, prediction, labels=[4], average='micro'),
    #                 'class_5_F1': f1_score(test_labels, prediction, labels=[5], average='micro'),
    #                 'accuracy': accuracy_score(test_labels, prediction)}

    #print('\nConfusion Matrix:')
    #print(confusion_matrix(test_labels, prediction, labels=[1, 2, 3, 4, 5]))

    # # Uncomment to print best 15 words.
    print('\nBest 15 Features:')
    print(best_features(vectorizer, train_vectors, train_labels))

    print()

    return test_results


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    results = classify(config['train_data'], config['test_data'])

    for k, v in results.items():
        print(k, v)
