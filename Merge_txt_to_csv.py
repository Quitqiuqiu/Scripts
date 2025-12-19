import os
import glob
import csv

def merge_txt_to_csv(input_dir, output_csv, include_filename=False):
    """
    将指定目录下的所有txt文件合并为一个CSV文件，尝试多种编码读取。

    参数：
    input_dir: txt文件所在目录
    output_csv: 输出的CSV文件名
    include_filename: 是否在CSV中包含文件名列（默认False）
    """

    encodings_to_try = ['gbk', 'utf-8', 'big5', 'latin-1']

    with open(output_csv, 'w', newline='', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # 写入标题行（可选）
        if include_filename:
            writer.writerow(['filename', 'content'])
        else:
            writer.writerow(['content'])

        # 获取目录下的所有 .txt 文件列表
        txt_files = glob.glob(os.path.join(input_dir, '*.txt'), recursive=False)

        if not txt_files:
            print(f"警告：目录 '{input_dir}' 中没有找到任何 .txt 文件。")
            return # 如果没有找到文件，直接返回
        print(f"在目录 '{input_dir}' 中找到 {len(txt_files)} 个 .txt 文件。")

        for file_path in txt_files:
            filename = os.path.basename(file_path)
            content = None
            decoded_successfully = False

            # 尝试使用不同的编码读取文件
            for encoding in encodings_to_try:
                try:
                    with open(file_path, 'r', encoding=encoding) as txtfile:
                        content = txtfile.read().strip()
                        decoded_successfully = True
                        break 
                except UnicodeDecodeError:
                    # 当前编码解码失败，尝试下一个编码
                    continue
                except Exception as e:
                    # 捕获除 UnicodeDecodeError 以外的其他文件读取错误 (如权限问题)
                    print(f"错误：读取文件 {filename} 失败 - {str(e)}")
                    decoded_successfully = False # 确保标记为失败
                    break # 发生其他错误，停止尝试当前文件

            # 如果成功解码，则写入CSV
            if decoded_successfully:
                try:
                    if include_filename:
                        writer.writerow([filename, content])
                    else:
                        writer.writerow([content])
                except Exception as e:
                    print(f"错误：写入文件 {filename} 的内容到CSV失败 - {str(e)}")
            else:
                 print(f"警告：文件 {filename} 编码异常或尝试的编码不匹配，已跳过。尝试的编码：{', '.join(encodings_to_try)}")

        print(f"所有文件处理完毕，结果已写入到 '{output_csv}'。")

merge_txt_to_csv(
    input_dir='D:\\Data\\Machine Learning\\中文文本分类项目数据集\\test_corpus',
    output_csv='C:\\Users\\Qiu\\Desktop\\test_corpus.csv',
    include_filename=True
)