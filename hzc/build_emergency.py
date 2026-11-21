# -*- coding: utf-8 -*-
"""生成「考前急救」1000 个易错字（全部来自 5500 字表，可核验）。

A. 形近易混（人工整理，常见易写错组）
B. 现代多音字（人工白名单，读音差别大、易读错）
C. 不足部分用乙表、丙表字补齐（生僻易忘）
"""
import json, re

chars = json.load(open('chars.json', encoding='utf-8'))
jia, yi, bing = chars['jia'], chars['yi'], chars['bing']
allc = jia + yi + bing
pos = {c: i for i, c in enumerate(allc)}

def uniq(s):
    out = []
    for c in s:
        if '\u4e00' <= c <= '\u9fff' and c not in out:
            out.append(c)
    return out

XING = """
己已巳未末士土日曰戊戌戍戒戎祟崇汨汩盲肓亳毫茶荼剌刺辨辩辫瓣拆折拔拨具俱藉籍
慕幕墓暮躁燥噪磬罄竣峻浚悟晤惟唯维绽锭揣惴湍暇遐瑕诞涎矫娇骄忸纽咄拙缀辍啜
掂惦踮拣捡副幅辐睬踩徽微撼憾概慨陡徒冶治薄簿靡糜顶鼎摧催弛驰诵颂阙阕篑匮馈
溃聩巅颠慑摄蓑衰沧苍沦伦抡轮纶囵鲠梗埂哽赓庚锲契挈楔戮戳弑试拭轼畴筹踌俦涛
滔韬蹈稻悼棹稔念捻拈嫣焉腌阉淹俺掩庵谙暗黯澡藻缲缫骚搔蚤庇疵纰批砒蚍毗枇琵
秕妣怙祜岵骷枯沽姑咕估菇菰辜感减碱缄箴涵函菡颔骁饶挠绕荛娆桡铙涂途徒屠脾啤
裨俾椑漕槽嘈艚糟遭驯训汛讯迅
"""

DUO = """
差强参着塞处传大当倒得的地调都度恶发分干更冠好号和会几假间将教结解尽卷看空
累量论落难宁弄迫铺圈散丧少舍省数说似宿提挑吐为系鲜相兴行血咽要应与载藏扎长
朝折正只种重属转畜蓄拗薄堡曝屏剥泊刹禅颤场车称乘澄冲臭创攒答逮单弹钉斗读肚
坊缝脯颈供勾骨广龟还巷横哄华混夹嚼角侥芥劲壳勒擂撩咧溜笼露抹埋蔓蒙眯磨模朴
雀扫煞厦杉蛇盛识缩帖拓瓦尾吓削校燕佣晕轧粘挣症中轴钻
掰板磅刨奔臂扁便别拨伯簸卜曾叉杈查茬岔柴嘲匙仇喘串吹戳绰刺撮搓打担挡灯跌兑
蹲顿夺番否夫服赶钢岗梗估谷观归过哈汗喝后呼划晃豁击家脚搅倔菌卡咳可抠扣枯苦
裤夸块冷俩连搂靡闷拧挪哦扒爬拍栖嚷扇刷塔台作
"""

sel, seen = [], set()
def add(src, cat):
    for c in uniq(src):
        if c in seen or c not in pos:
            continue
        seen.add(c)
        sel.append((c, cat))

add(XING, '形近')
add(DUO, '多音')
# 补齐：乙表 → 丙表
add(yi, '生僻')
add(bing, '生僻')

sel = sel[:1000]
from collections import Counter
cnt = Counter(k for _, k in sel)
print('合计', len(sel), dict(cnt))

data = {'idx': [pos[c] for c, _ in sel], 'cat': [k for _, k in sel]}
json.dump(data, open('emergency.json', 'w', encoding='utf-8'), ensure_ascii=False)
