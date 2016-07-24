import matplotlib.pyplot as plt
import numpy as np

def bar_percentage(series,bar_width=0.5,xlabel_font=12,ylim=(0,1)):
    # series should have pandas.Series interface
    # return a plot of probabilities
    
    fig = plt.figure()
    ax  = fig.add_subplot(111,aspect=len(series)-1)
    ax.set_ylim(ylim)
    ax.axhline(0,c="black")
    ax.set_ylabel("Percentage",fontsize=14)
    
    # enumerate series.index and plot series.value on top
    x = np.array(range(len(series.index)))
    ax.bar(x,series.values,bar_width,fill=False, hatch='\\',color=None)
    
    # format x axis
    ax.set_xticks(x)
    ax.set_xlim(min(x)-bar_width/2.,max(x)+bar_width*1.5)
    ax.set_xticklabels(series.index,fontsize=xlabel_font,rotation=45)
    
    fig.tight_layout()
    return fig,ax
# end def 
