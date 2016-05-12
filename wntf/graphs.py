import matplotlib.pyplot as plt
from wordcloud import WordCloud


def word_cloud(f):
    wordcloud = WordCloud().generate_from_frequencies(f)
    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('out/word_cloud.png', dpi=300, format='png')