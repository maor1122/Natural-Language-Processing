# Natural Language Processing
This repository contains some of the projects I liked from the NLP course in my degree.

## Cloze Solver

This is a simple cloze solver project where we fill out missing words out of paragraph given a paragrapth and the missing words in random order.
for example for this paragraph:
<br><code>The wooden bridge, dating from the Middle Ages, across the Aare was destroyed by
floods three __________ in thirty years, and was replaced with a steel suspension
__________ in 1851. This was replaced by a __________ bridge in 1952. The city was
linked up to the Swiss Central Railway in 1856.</code><br>
This should be the output:
<br><code>\[‘times’, ‘bridge’, ‘concrete’\]</code><br>
The simple solution we used to this problem is using an improved bigram language model by learning from a large lexicon and then checking for each word, but instead of checking only the previous word we check the next word aswell.
<br>
I used mainly python for this project without any importent external libraries.<br>

## Amazon Reviews Rating Classification

The goal of this project was to build a text classification model that predicts a product’s rating (1–5) from its review text.
I worked with a dataset of Amazon product reviews across multiple categories, each containing:
- Review text and summary
- Reviewer info
- Verification flag
- Rating (overall) as the label

Each review was represented as:
<code> {"overall": 4.0, "verified": true, "reviewText": "...", "summary": "..."} </code>
The model will be trained on 10,000 reviews (2,000 per class) and tested on 2,000 reviews (400 per class).

#### Methodology

The model pipeline included:
1. Preprocessing and Filtering
- Only verified reviews were used.
- Each sample combined: summary + reviewText + unixReviewTime + reviewerName.
2. Feature Extraction
- Used CountVectorizer from scikit-learn to convert text into a bag-of-words representation.
- Experimented with unigrams (1-gram) and TF-IDF weighting, but final results used only unigrams — they performed best and trained faster.
3. Feature Selection
- Applied SelectKBest to select the 15 most informative words for each rating class.
- output: <code>'but', 'five', 'four', 'great', 'love', 'loves', 'money', 'not', 'one', 'perfect', 'star', 'stars', 'three', 'two', 'waste', 'ok' </code>
4. Classification Model
- Trained a Logistic Regression classifier on the extracted vectors.
- Evaluated model performance using accuracy, F1-score, and confusion matrix.
  
#### Results

Confusion Matrix:
<br><code>Predicted →
True ↓ 
    224  83  20  12  10
    87 183  64  19  10
    47  77 165  48  27
    11  39  77 170  72
    15  20  19  47 272
</code><br>

prediction accuracy for each class (/rating)
1 rating: 61%
2 rating: 48%
3 rating: 47%
4 rating: 51%
5 rating: 71%
average accuracy for exact rating: 56%

I mainly used python, sklearn and numpy for this project.<br>
