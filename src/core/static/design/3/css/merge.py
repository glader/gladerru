import os
import re


def insert_style(result):
    style = result.group(1)
    print("process " + style)
    css = re.sub('@import url\(([^\)]+?)\);', insert_style, open(style).read())
    return css


def merge_css(style):
    print("merge " + style)
    css = re.sub('@import url\(([^\)]+?)\);', insert_style, open(style).read())
    css = re.sub("\n", " ", css)
    css = re.sub("\s+", " ", css)
    new_style_name = re.sub('\.css', '_.css', style)
    open(new_style_name, 'w').write(css)


for style in os.listdir('.'):
    if not style.endswith('.css') or style.endswith('_.css'):
        continue
    merge_css(style)
