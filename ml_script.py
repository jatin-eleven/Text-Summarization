
"""
EXTRACTIVE TEXT SUMMARIZATION 

How to do Text Summarization :
    - Text Cleaning
    - Sentance Tokenization
    - Word Tokenization
    - Word-Frequency Table
    - Summarization
"""

# python -m spacy download en_core_web_sm 

import spacy
from spacy.lang.en.stop_words import STOP_WORDS

from heapq import nlargest


# # --------------------------------
# from spacy import load
# # --------------------------------

def Text_Summarization(text):

    from string import punctuation
    
    import en_core_web_sm
    nlp = en_core_web_sm.load()

    # nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    stopwords = list(STOP_WORDS)

    # formation of tokens from the text
    tokens = [token.text for token in doc]


    punctuation = punctuation + "\n"


    word_frequency = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation and word.text.lower() not in "\n":
                if word.text not in word_frequency.keys():
                    word_frequency[word.text] = 1
                else:
                    word_frequency[word.text] += 1

    max_frequency = max(word_frequency.values())


    # # for getting the NORMALIZED FREQUENCY we will divide the each word frequency by max_frequency
    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word]/max_frequency




    # # # ---------------------------- SENTANCE TOKENIZATION -----------------------------------
    sentance_tokens = [sent for sent in doc.sents]

    sentance_scores = {}
    for sent in sentance_tokens:
        for word in sent:
            if word.text in word_frequency.keys():
                # # here adding the normalized frequency of each word present in the sentances
                # # and store in the sentance_score dict....
                # # eg : NF(word1) + NF(word2) + NF(word3)
                if sent not in sentance_scores.keys():
                    sentance_scores[sent] = word_frequency[word.text]
                else:
                    sentance_scores[sent] += word_frequency[word.text]



    # # getting the 30% of the sentance
    select_length = int(len(sentance_tokens)*0.3)


    # # finding the largest sentace_score sentance in the text...
    summary = nlargest(select_length, sentance_scores, key=sentance_scores.get)


    # # maintaining the order of the sentance
    # # order will define meaning of the sentances in summary...
    indexing = []
    for i in summary:
        for j in range(len(sentance_tokens)):
            if str(i) == str(sentance_tokens[j]) and str(i) not in indexing:
                indexing.append(j)
                break 
    # removing the repeated sentances...
    indexing = set(indexing)


    final_summary = []
    for i in indexing:
        final_summary.append(str(sentance_tokens[i]))


    summary = ' '.join(final_summary)
    # print("\n\nSUMMARY : \n", summary, "\n\n")
    return summary

