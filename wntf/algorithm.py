# -*- coding: utf-8 -*-
import nltk


def tag(lines):
    try:
        tokenized_words = nltk.word_tokenize(lines)
        return nltk.pos_tag(tokenized_words)
    except LookupError as le:
        print("Run install_words.py first")
        raise le


def nouns(tagged_text):
    return findtags('NN', tagged_text)


def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
        if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].most_common(20)) for tag in cfd.conditions())
