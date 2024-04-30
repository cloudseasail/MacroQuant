
import matplotlib.pyplot as plt

import numpy as np
def random_color():
    return '#%06x' % np.random.randint(0, 0xFFFFFF)
def random_colorArr(N):
    colorArr=[]
    for i in range(N):
        colorArr.append(random_color())
    return colorArr

def plot_twins_ax(xlabel=None,ylabel1=None,ylabel2=None,len_xticks=10,figsize=(10,6)):
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    fig=plt.figure(figsize=figsize)
    ax1=plt.subplot2grid((1,1),(0,0),rowspan=1,colspan=1)
    ax1.set_ylabel(ylabel1)
    # ax1.set_xticks(data.index[xticks])
    plt.xticks(rotation=30)

    ax2=ax1.twinx()
    # ax2.legend(loc='upper left')
    ax2.set_ylabel(ylabel2)
    ax2.set_xlabel(xlabel)
    ax2.grid(True,alpha=0.2)
    return (ax1, ax2)


def plot_bar_line(bar, line, title=""):
    (ax1, ax2) = plot_twins_ax('', bar.name, line.name)
    bar.plot(kind='bar', ax=ax1)
    line.plot(ax=ax2,legend=True, color='r', title=title)