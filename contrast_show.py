import xml.etree.ElementTree as ET  # 读取xml。
import os
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt


def parse_rec(filename):
    tree = ET.parse(filename)  # 解析读取xml函数
    objects = []
    img_dir = []
    for xml_name in tree.findall('filename'):
        img_path = os.path.join(pic_path, xml_name.text)
        img_dir.append(img_path)
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)

    return objects, img_dir


# 可视化
def visualise_gt(objects, img_dir):
    for id, img_path in enumerate(img_dir):
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        for a in objects:
            xmin = int(a['bbox'][0])
            ymin = int(a['bbox'][1])
            xmax = int(a['bbox'][2])
            ymax = int(a['bbox'][3])
            label = a['name']
            draw.rectangle((xmin, ymin, xmax, ymax), fill=None, outline=(0, 255, 0), width=2)
            draw.text((xmin - 10, ymin - 15), label, fill=(0, 255, 0))  # 利用ImageDraw的内置函数，在图片上写入文字
        img.show()


# fontPath = "/Users/duanhan/Downloads/consola.ttf"  # 字体路径
root = 'E:/PycharmProjects/faster-rcnn-pytorch/NEU-DET'
# ann_path = os.path.join(root, 'ANNOTATIONS/')  # xml文件所在路径
gt_path = "./input/ground-truth"
dr_path = "./input/detection-results"
pic_path = 'E:/PycharmProjects/faster-rcnn-pytorch/NEU-DET/IMAGES/' # 样本图片路径
# print(pic_path)
# font = ImageFont.truetype(fontPath, 16)

for filename in os.listdir(gt_path):
    gtfilename = gt_path + '/' + filename
    drfilename = dr_path + '/' + filename
    imgfilename = filename.replace('txt', 'jpg')
    img_path = pic_path + imgfilename
    txtf = open(gtfilename, 'r')
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    for line in txtf:
        # print(line)
        line = line.split(' ')
        label = line[0]
        xmin = int(line[1])
        ymin = int(line[2])
        xmax = int(line[3])
        ymax = int(line[4])
        # print(label, xmin, ymin, xmax, ymax)
        draw.rectangle((xmin, ymin, xmax, ymax), fill=None, outline=(0, 255, 0), width=2)
        draw.text((xmin - 10, ymin - 15), label+'-gt', fill=(0, 255, 0))
    txtf.close()
    txtf = open(drfilename, 'r')
    for line in txtf:
        line = line.split(' ')
        # print(line)
        label = line[0]
        xmin = int(line[2])
        ymin = int(line[3])
        xmax = int(line[4])
        ymax = int(line[5])
        draw.rectangle((xmin, ymin, xmax, ymax), fill=None, outline=(255, 0, 0), width=4)
        draw.text((xmin - 10, ymin - 15), label + '-dr', fill=(255, 0, 0))
    img.show()




