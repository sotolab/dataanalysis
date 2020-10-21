# -*- coding: utf-8 -*-
# Run >>  $ python allcloud.py

import sys
from wordcloud import WordCloud
import openpyxl
import pandas as pd
import allfname as fn
from collections import Counter

def main():

    filename = fn.allfname()

    for i in filename:
        wb = openpyxl.load_workbook(i+".xlsx")
        ws = wb.active
        list = []

        for r in ws.rows:
            # index = r[0].row
            txt = r[0].value
            # print("txt:", txt)
            list.append(str(txt))

        result = ",".join(list)
        # print("result:", result)

        count = Counter(list)
        # print(" count: ", count)
        tags = count.most_common(40)

        wc = WordCloud(font_path='C:\\Windows\\Fonts\\NGULIM.TTF', background_color='white', width=1000, height=1000, max_words=1000, max_font_size=300)
        # wc.generate(str(result))
        wc.generate_from_frequencies(dict(tags))
        wc.to_file(i+'_world.png')
        print(i+" done")

if __name__ == "__main__":
    main()
    print("All done")
