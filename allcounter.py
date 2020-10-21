# -*- coding: utf-8 -*-
# Run >>  $ python allcounter.py
import sys
from wordcloud import WordCloud
import openpyxl
import pandas as pd
from pandas import DataFrame as df
import re
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
from konlpy.tag import Hannanum
import allfname as fn

# filename = sys.argv[1]
# MALL_SIZE = 8
# MEDIUM_SIZE = 10
# BIGGER_SIZE = 12
#
# plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
# plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
# plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# fig = plt.figure()
# fig.suptitle('test title', fontsize=20)
# plt.xlabel('xlabel', fontsize=18)
# plt.ylabel('ylabel', fontsize=16)

# params = {'legend.fontsize': 'x-large',
#           'figure.figsize': (15, 5),
#          'axes.labelsize': 'x-large',
#          'axes.titlesize':'x-large',
#          'xtick.labelsize':'x-large',
#          'ytick.labelsize':'x-large'}
# plt.rcParams.update(params)

font_location = "c:/Windows/fonts/HMFMMUEX.TTC"
font_name = font_manager.FontProperties(fname=font_location).get_name()
font = {'family' : font_name,
        'weight' : 'bold',
        'size'   : 15}
# matplotlib.rc('font', **font)


def showGraph(wordInfo, filename ):

    matplotlib.rc('font', **font) #family=font_name, size=15)

    plt.figure(figsize=(20,10))

    plt.xlabel('해시태크')
    plt.ylabel('빈도수')
    plt.grid(True)

    Sorted_Dict_Values = sorted(wordInfo.values(), reverse=True)
    Sorted_Dict_Keys = sorted(wordInfo, key=wordInfo.get, reverse=True)

    plt.bar(range(len(wordInfo)), Sorted_Dict_Values, align='center')
    plt.xticks(range(len(wordInfo)), list(Sorted_Dict_Keys), rotation='70')

    plt.savefig(filename+"_counter"+'.png', dpi=300)

    # plt.show()

def main():

    filename = fn.allfname()
    # print("filename:", filename)

    for i in filename:
        wb = openpyxl.load_workbook(i+".xlsx")
        ws = wb.active

        list = []

        for r in ws.rows:
            index = r[0].row
            txt = r[0].value
            # print("txt:", txt)
            list.append(str(txt))

        result = ",".join(list)
        # print("result:", result)

        #-------------------------
        result = re.sub('[0-9]+', '', result)
        result = re.sub('[A-Za-z]+', '', result)
        result = re.sub('[-_]', '', result)
        # result = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》]', '', result)

        result = result.replace(',', ' ')

        # ----------------------------
        nlp = Okt()
        nouns = nlp.nouns(result)
        count = Counter(nouns)

        # print(text_list)

        names = []
        values = []

        wordInfo = dict()
        for tags, counts in count.most_common(50):
            if (len(str(tags)) > 2):
                wordInfo[tags] = counts
                names.append(str(tags))
                values.append(counts)
                # print ("%s : %d" % (tags, counts))

        showGraph(wordInfo, i)

        df1 = df(data = {'Tag': names, 'Value': values  })
        # print (" df1 %s" % df1)
        df1.to_excel(i+"DataFrame"+'.xlsx')

        print( i + "  done")




if __name__ == "__main__":
    main()
    print("All done")
