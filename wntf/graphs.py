import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy


def word_cloud(f):
    wordcloud = WordCloud().generate_from_frequencies(f)
    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('out/word_cloud.png', dpi=300, format='png')


def wheel_radii(wheel, name):
    cnt = len(wheel['pattern'].keys())
    if cnt == 0:
        return
    N = cnt
    theta = numpy.linspace(0.0, 2*numpy.pi, N, endpoint=False)
    radii = [item['count'] for key, item in wheel['pattern'].items()]
    width = numpy.pi * 2 / N

    ax = plt.subplot(111, projection='polar')
    bars = ax.bar(theta, radii, width=width, bottom=0.0)
    for r, theta, bar, key in zip(radii, theta, bars, [key for key, item in wheel['pattern'].items()]):
        bar.set_label(name)
        bar.set_facecolor(plt.cm.jet(r / 10.))
        bar.set_alpha(0.5)
        if r > 0:
            ax.annotate(
                key, (theta, r), xytext=(15, 15),
                textcoords='offset points',
                arrowprops=dict(facecolor='black', shrink=0.05),)
    plt.title(name)
    plt.savefig('out/wheel_%s.png' % name, dpi=300, format='png')
    plt.show()