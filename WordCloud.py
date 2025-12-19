import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import numpy as np
plt.rcParams['font.sans-serif'] = ['SimHei']

# 1. 准备停用词和分词函数
# 创建停用词表
stopwords = {}.fromkeys([line.rstrip() for line in
                          open(r"D:\Data\\hlt_stop_words.txt",
                               encoding='gb18030')])

# 自定义停用词
custom_stop_words = [' ', ',', '\n']
for w in custom_stop_words:
    if w not in stopwords:
        stopwords[w] = None

# 定义分词函数
def text_preprossing(context):
    """
    对输入的中文文本进行分词和停用词过滤。
    """
    words_cut = jieba.cut(context, cut_all=False)
    filtered_words = [item for item in words_cut
                      if item not in stopwords and not item.isdigit()]
    return ' '.join(filtered_words)

# 2. 读取文本文件并处理
file_path = "C:\\Users\\Quitqiuqiu\\Desktop\\test.txt"  # txt文件路径

if not os.path.exists(file_path):
    print(f"错误：文件不存在，请检查路径。{file_path}")
else:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
    except Exception as e:
        print(f"读取文件失败，可能编码不正确。尝试使用 'gb18030' 编码。")
        try:
            with open(file_path, 'r', encoding='gb18030') as f:
                text_content = f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            text_content = ""

    if text_content:
        processed_text = text_preprossing(text_content)

        # 3. 生成词云图
        font_path = "C:\\Windows\\Fonts\\微软雅黑\\Microsoft YaHei Bold" 
        if not os.path.exists(font_path):
            print(f"警告：找不到中文字体文件 '{font_path}'。请检查路径并将其替换为可用的中文字体。")
            print("如果缺失，词云图中的中文可能无法正常显示。")
            font_path = None

        # 创建词云对象
        wordcloud = WordCloud(
            font_path=font_path,
            width=1200,
            height=1000,
            background_color='white',  # 背景颜色
            colormap='turbo_r',        # 词语颜色
            max_words=500,              # 最大词数
            margin = 5,                # 间距
            # mask=mask_image,         # 可选：词云形状蒙版
            stopwords=stopwords,       # 传入停用词，虽然分词函数已过滤，但这里可以再次过滤
            contour_width=3,
            contour_color='steelblue'
        ).generate(processed_text)

        # 4. 显示词云图
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # 隐藏坐标轴
        # plt.title('词云图', fontsize=20)
        plt.show()