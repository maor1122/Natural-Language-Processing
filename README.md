# Natural Language Processing
This repository contains some of the projects I liked from the NLP course in my degree.

## Cloze Solver

This is a simple cloze solver project where we fill out missing words out of paragraph given a paragrapth and the missing words in random order.
for example for this paragraph:
<br><code>The wooden bridge, dating from the Middle Ages, across the Aare was destroyed by
floods three __________ in thirty years, and was replaced with a steel suspension
__________ in 1851. This was replaced by a __________ bridge in 1952. The city was
linked up to the Swiss Central Railway in 1856.</code><br>
this should be the output output:
<br><code>\[‘times’, ‘bridge’, ‘concrete’\]</code><br>
The simple solution we used to this problem is using an improved bigram language model by learning from a large lexicon and then checking for each word, but instead of checking only the previous word we check the next word aswell.
