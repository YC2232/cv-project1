import xml.etree.ElementTree as ET
import os

def convert_voc_to_yolo(xml_file, txt_file, classes):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(txt_file, 'w') as f:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = ((b[0] + b[1]) / (2 * w), (b[2] + b[3]) / (2 * h),
                  (b[1] - b[0]) / w, (b[3] - b[2]) / h)
            f.write(f'{cls_id} {" ".join([str(a) for a in bb])}\n')

# 类别列表
classes = ['ffe']  # 根据您的类别进行修改

# 转换指定目录下的所有 XML 文件
xml_dir = r'C:\Users\28482\Desktop\cv-project\cv-project\distinguish-img\labels\val'
txt_dir = r'C:\Users\28482\Desktop\cv-project\cv-project\distinguish-img\labels\val'

if not os.path.exists(txt_dir):
    os.makedirs(txt_dir)

for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        txt_file = xml_file[:-4] + '.txt'
        convert_voc_to_yolo(os.path.join(xml_dir, xml_file), os.path.join(txt_dir, txt_file), classes)
