===============================
Who Not to Follow
===============================

Twitter has a recommendation algorithm. Based on who you follow and your description it recommends more people that you might find interesting.

This is really helpful, allows you to build up a lot of followers (or followees) in your world, but there is one fatal flaw in the algorithm.

It assumes you want to follow people who are all more or less the same. I realised that the 1,000 people I am following on twitter are guys, in their 20's and 30's, with kids,
interesting in cloud, technology, programming and Python. So basically copies of myself. What am I really going to learn from them? Sure I'll polish my technical
skills and find out about the lastest cool new utility and project going around. But it won't expand my world view on anything and I'll become a more narrow minded individual.

.. image:: https://img.shields.io/pypi/v/wntf.svg
        :target: https://pypi.python.org/pypi/wntf

.. image:: https://img.shields.io/travis/tonybaloney/wntf.svg
        :target: https://travis-ci.org/tonybaloney/wntf

.. image:: https://readthedocs.org/projects/wntf/badge/?version=latest
        :target: https://readthedocs.org/projects/wntf/?badge=latest
        :alt: Documentation Status


An anti-recommendation algorithm for twitter

* Free software: ISC license
* Documentation: https://wntf.readthedocs.org.

How it works
------------

I initially thought I could just search for the opposite (antonym) of my profile and search for that. It's not that simple! What is the opposite of 'enthusiast' and does that even make sense?

The algorithm takes the profile description of your followers on Twitter, uses a natural language processing tool (NLTK) to understand characteristics
of your followers.

The first thing to look at is the nouns in the followers description and the most common nouns. For me, this is :


    {'NN': [('https', 80),
        ('cloud', 56),
        ('@', 39),
        ('technology', 36),
        ('http', 31),
        ('software', 30),
        ('developer', 28),
        ('business', 28),
        ('world', 26),
        ('father', 24),
        ('news', 23),
        ('fan', 21),
        ('account', 20),
        ('source', 20),
        ('husband', 20),
        ('enthusiast', 18),
        ('team', 18),
        ('web', 18),
        ('geek', 17),
        ('code', 17)],
        }

So what can we tell about those nouns?

We then filter out certain nouns that commonly occur, such as 'tweet', 'views', 'opinions', since a lot of people have a statement about their views not representing
their employer etc. etc.

Once you filter that list I can see that my followers' characteristics in a few traits:

 - Their industry 'business', 'technology'
 - Their role 'developer'
 - Their gender 'husband', 'father'
 - Their interests 'web', 'code', 'software'
 - The way they describe themselves 'geek', 'enthusiast'

Looking at the Proper nouns I can also get some other interesting information:

    'NNP': [('@', 313),
        ('Cloud', 92),
        ('|', 74),
        ('Data', 63),
        ('IT', 44),
        ('Dimension', 39),
        ('Software', 36),
        ('Microsoft', 35),
        ('Director', 35),
        ('Python', 32),
        ('Manager', 31),
        ('Husband', 26),
        ('Developer', 25),
        ('CTO', 25),
        ('Architect', 25),
        ('CEO', 24),
        ('Engineer', 24),
        ('/', 24),
        ('Technology', 23),
        ('Dad', 23)],

Again filtering out some of the fluff, like @ and `/`

 - Company data Microsoft, Dimension (Data)
 - Role 'CTO', 'CEO', Engineer, Architect

Now for each of these words we build up a synset. A Synset is a set of synonyms that share a common meaning. So for 'technology', the synset includes the nouns 'technology' and 'engineering'.

Then we look at the following characteristics of the word 'technology':

- The hypernyms, in this case 'application' and 'profession' (we are interested in this)
- The hyponyms (subsets), 'aeronautical engineering', 'automotive technology' 'chemical engineering' etc.

The diversity wheel
-------------------

.. image:: http://web.jhu.edu/sebin/t/m/DiversityWheel_Small.jpg

The diversity wheel has many characterstics,  such as :

- gender
- background
- interests
- religion

If we put the nouns into buckets in the diversity wheel based on their hypernyms then we find a better view of your following.

Also, we don't want to assume that all of your followers are the same, so we'll weight each instance based on it's frequency.

TODO
----
This is half finished (my flight leaves soon):

- build up a map of wheels and the words in those wheels (e.g professions, regligion, interests)
- map those in a chord where the size of the difference between the angles in the chord represents the difference, e.g. carpenter is very different to IT, but banker is similar to accountant
- rank all your words into the chords, show the chord diagrams and then plot points furthest away and use those words to make recommendations.

The wheels will represent the diversity wheel (http://web.jhu.edu/sebin/t/m/DiversityWheel_Small.jpg)

Credits
---------

This package was created with Cookiecutter_ and (a fork of) the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`tonybaloney/cookiecutter-pypackage`: https://github.com/tonybaloney/cookiecutter-pypackage
