# -*- coding: utf-8 -*-
"""生成静态「1000 易错字」页：纯文本，最容易被搜索引擎收录。"""
import json, re

chars = json.load(open('chars.json', encoding='utf-8'))
allc = chars['jia'] + chars['yi'] + chars['bing']
em = json.load(open('emergency.json', encoding='utf-8'))

pin = {}
for line in open('pinyin.txt', encoding='utf-8'):
    m = re.match(r'U\+([0-9A-F]+):\s*([^#]+)#', line)
    if not m:
        continue
    ch = chr(int(m.group(1), 16))
    rs = []
    for p in m.group(2).split(','):
        p = p.strip()
        if p and p not in rs:
            rs.append(p)
    pin[ch] = rs

groups = {'形近': [], '多音': [], '生僻': []}
for i, cat in zip(em['idx'], em['cat']):
    c = allc[i]
    groups.setdefault(cat, []).append((c, pin.get(c, [''])[0]))

titles = {
    '形近': ('形近易混字', '容易写错、看错的一组组字：己/已/巳、戊/戌/戍、辨/辩/辫/瓣、拔/拨、薄/簿……'),
    '多音': ('多音易读字', '一个字有多个读音，读错多半是因为没分清它在词里的意思：差、强、塞、着、薄……'),
    '生僻': ('生僻易忘字', '来自测试字表乙表、丙表的字，日常不常见，考试里最容易丢分。'),
}

rows = []
for k in ['形近', '多音', '生僻']:
    t, d = titles[k]
    items = ''.join(
        f'<span class="c" title="{r}"><b>{c}</b><i>{r}</i></span>' for c, r in groups[k]
    )
    rows.append(f'<section><h2>{t}（{len(groups[k])} 字）</h2><p>{d}</p><div class="grid">{items}</div></section>')

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>1000个易错字表（形近·多音·生僻）｜汉字应用水平测试考前急救</title>
<meta name="description" content="整理自《汉字应用水平测试字表》的1000个易错字：225个形近易混字、261个多音易读字、514个生僻易忘字，附拼音，适合考前速览。">
<meta name="keywords" content="易错字,1000个易错字,形近字,多音字,生僻字,汉字应用水平测试,错别字">
<meta name="robots" content="index,follow">
<link rel="canonical" href="https://entiesci.github.io/OnlineTest/hzc/1000easywrong.html">
<style>
body{{margin:0;background:#f6f1e7;color:#211c16;font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.9}}
.wrap{{max-width:860px;margin:0 auto;padding:40px 22px 80px}}
h1{{font-size:26px;margin:0 0 8px;letter-spacing:.03em}}
.sub{{color:#6b6255;font-size:13.5px;margin:0 0 8px}}
a.back{{display:inline-block;margin:14px 0 26px;background:#211c16;color:#fff;text-decoration:none;padding:10px 22px;border-radius:10px;font-size:14px}}
section{{margin:0 0 34px;border-top:1px solid #e4dbc9;padding-top:20px}}
h2{{font-size:17px;margin:0 0 6px}}
section p{{color:#6b6255;font-size:13px;margin:0 0 14px}}
.grid{{display:flex;flex-wrap:wrap;gap:8px}}
.c{{display:inline-flex;flex-direction:column;align-items:center;width:58px;padding:8px 0;border:1px solid #e4dbc9;border-radius:9px;background:#fffdf8}}
.c b{{font-family:"KaiTi","Kaiti SC",serif;font-size:24px;font-weight:400;line-height:1.2}}
.c i{{font-style:normal;font-size:10.5px;color:#9a9082;margin-top:2px}}
footer{{margin-top:40px;color:#9a9082;font-size:12px;border-top:1px solid #e4dbc9;padding-top:16px}}
</style>
</head>
<body>
<div class="wrap">
<h1>1000 个易错字表</h1>
<p class="sub">整理自《汉字应用水平等级及测试大纲》附录 A《汉字应用水平测试字表》：225 个形近易混字、261 个多音易读字、514 个生僻易忘字，共 1000 字，附常用读音。</p>
<a class="back" href="./">去在线测试 →</a>
{''.join(rows)}
<footer>字表依据《汉字应用水平等级及测试大纲》（GF 2002—2013）附录 A；拼音为常用读音，多音字以常用读法标注。本页为静态索引页，配套在线测试见 <a href="./">汉字应用水平测试 5500 字通关</a>。</footer>
</div>
</body>
</html>'''
open('1000easywrong.html', 'w', encoding='utf-8').write(html)
print('ok', len(html), len(groups['形近']), len(groups['多音']), len(groups['生僻']))
