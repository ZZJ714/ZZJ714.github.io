# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:08:03 2021

@author: zzj
"""

import jieba
import jieba.posseg as pseg

word_name_list={'林黛玉',
           '薛宝钗',
           '史湘云',
           '王熙凤',
           '贾元春',
           '贾探春',
           '贾惜春',
           '贾迎春',
           '妙玉',
           '李纨',
           '秦可卿',
           '贾巧姐'}

# 输入文件
txt_file_name = './data/红楼梦.txt'
# 输出文件
node_file_name = './data/红楼梦-人物节点.csv'
link_file_name = './data/红楼梦-人物连接.csv'

# 打开文件，读入文字
txt_file = open(txt_file_name, 'r', encoding='utf-8')
line_list = txt_file.readlines()
txt_file.close()

# 加载用户字典
jieba.load_userdict('./data/自定义字典（原）.txt')

line_name_list = []  # 每个段落出现的人物列表
name_cnt_dict = {}  # 统计人物出现次数

print('正在分段统计……')
print('已处理词数：')
progress = 0  # 用于计算进度条
for line in line_list: # 逐个段落循环处理
    word_gen = pseg.cut(line) # peseg.cut返回分词结果，“生成器”类型
    line_name_list.append([])
    
    for one in word_gen:
        word = one.word
        flag = one.flag
        
        # 对指代同一人物的名词进行合并
        if word =='林妹妹'or word=='黛玉':
            word='林黛玉'
        elif word == '宝姐姐'or word=='宝钗':
            word = '薛宝钗'
        elif word == '巧姐儿'or word=='巧姐' :
            word = '贾巧姐'
        elif word =='惜春':
            word ='贾惜春'
        elif word =='探春':
            word ='贾探春'
        elif word == '迎春':
            word='贾迎春'
        elif word=='元春'or word=='元妃' :
            word = '贾元春'
        elif word=='凤姐' or word=='凤辣子' or word=='凤哥儿' or word=='凤姐儿':
            word='王熙凤'
        elif word=='可卿':
            word='秦可卿'
        elif word=='湘云' :
            word='史湘云'
            
        if word in word_name_list: 
            line_name_list[-1].append(word)
            if word in name_cnt_dict.keys():
                name_cnt_dict[word] = name_cnt_dict[word] + 1
            else:
                name_cnt_dict[word] = 1
        
        # 因为词性分析耗时很长，所以需要打印进度条，以免用户误以为死机了
        progress = progress + 1
        progress_quo = int(progress/1000)
        progress_mod = progress % 1000 # 取模，即做除法得到的余数
        if progress_mod == 0: # 每逢整千的数，打印一次进度
            #print('---已处理词数（千）：' + str(progress_quo))
            print('\r' + '-'*progress_quo + '> '\
                  + str(progress_quo) + '千', end='')
# 循环结束点        
print()
print('基础数据处理完成')

##--- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}


for line_name in line_name_list:
    for name1 in line_name:
        # 判断该人物name1是否在字典中
        if name1 in relation_dict.keys():
            pass  # 如果已经在字典中，继续后面的统计工作
        relation_dict[name1] = {}  # 添加到字典
        
        # 统计name1与本段的所有人名（除了name1自身）的共现数量
        for name2 in line_name:
            if name2 == name1:  
            # 不统计name1自身
                continue
            
            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

    
# 字典转成列表，按出现次数排序
item_list = list(name_cnt_dict.items())
item_list.sort(key=lambda x:x[1],reverse=True)

## 导出节点文件
node_file = open(node_file_name, 'w') 
# 节点文件，格式：Name,Weight -> 人名,出现次数
node_file.write('Name,Weight\n')
node_cnt = 0  # 累计写入文件的节点数量
for name,cnt in item_list: 
    node_file.write(name + ',' + str(cnt) + '\n')
    node_cnt = node_cnt + 1
node_file.close()
print('人物数量：' + str(node_cnt))
print('已写入文件：' + node_file_name)


link_file = open(link_file_name, 'w')
# 连接文件，格式：Source,Target,Weight -> 人名1,人名2,共现数量
link_file.write('Source,Target,Weight\n')
link_cnt = 0  # 累计写入文件的连接数量
for name1,link_dict in relation_dict.items():
    for name2,link in link_dict.items():
        link_file.write(name1 + ',' + name2 + ',' + str(link) + '\n')
        link_cnt = link_cnt + 1
link_file.close()
print('连接数量：' + str(link_cnt))
print('已写入文件：' + link_file_name)   