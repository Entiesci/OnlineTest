# -*- coding: utf-8 -*-
import json, re, random

# ---------- 1. 字表 ----------
chars = json.load(open('chars.json', encoding='utf-8'))
groups = {k: chars[k] for k in ['jia', 'yi', 'bing']}
all_chars = groups['jia'] + groups['yi'] + groups['bing']

# ---------- 2. 拼音 ----------
pin = {}
for line in open('pinyin.txt', encoding='utf-8'):
    m = re.match(r'U\+([0-9A-F]+):\s*([^#]+)#', line)
    if not m:
        continue
    ch = chr(int(m.group(1), 16))
    rs = [p.strip() for p in m.group(2).split(',') if p.strip()]
    seen, out = set(), []
    for r in rs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    pin[ch] = out

# ---------- 3. 字典 ----------
dic = {}
for it in json.load(open('xinhua_word.json', encoding='utf-8')):
    w = it.get('word', '')
    if w and len(w) == 1:
        dic[w] = it

CITE = re.compile(r'[《》]|--|——')
SENSE = re.compile(r'^[①-⑳⒈-⒛]')


def clean_gloss(ch, text):
    """从新华字典解释中提取一条现代义项，返回短释义或 None"""
    t = text.replace('\r', '')
    lines = [l.strip() for l in t.split('\n')]
    cands = []
    for l in lines:
        if not l or len(l) < 3:
            continue
        if CITE.search(l):
            continue
        if l.startswith('【'):          # 词条
            continue
        if '同本义' in l or '本义' in l and len(l) < 12:
            continue
        if SENSE.match(l):
            cands.append(l)
    if not cands:
        # 退化：找第一条没有书名号/引文的释义行
        for l in lines:
            if 4 <= len(l) <= 40 and not CITE.search(l) and not l.startswith('【') \
               and '--' not in l and '。' in l or (4 <= len(l) <= 30 and not CITE.search(l) and not l.startswith('【')):
                cands.append(l)
                break
    if not cands:
        return None
    g = cands[0]
    g = re.sub(r'^[①-⑳⒈-⒛]\s*', '', g)
    # 去掉 ～ 例句：截断
    if '～' in g:
        g = g.split('～')[0]
    g = re.sub(r'[（(][^）)]*[）)]', '', g)
    g = g.strip(' ，。、；：:;,')
    # 只保留第一小句
    for sep in ['。', '；', ';', '，', ',']:
        if sep in g:
            g = g.split(sep)[0]
            break
    g = g.strip(' ，。、；：:;,')
    if len(g) < 3 or len(g) > 24:
        return None
    if CITE.search(g) or '～' in g:
        return None
    return g


def clean_gloss2(ch, text):
    """第二遍：从 ～ 例句段中提取释义"""
    t = text.replace('\r', '')
    for l in [x.strip() for x in t.split('\n')]:
        if 4 <= len(l) <= 26 and not CITE.search(l) and not l.startswith('【') \
           and '同本义' not in l and '本义' not in l and '又如' not in l \
           and re.search(r'[\u4e00-\u9fff]', l) and '，' not in l[:2]:
            return None
    return None


gloss = {}
words = {}
for ch in all_chars:
    it = dic.get(ch)
    if not it:
        continue
    g = clean_gloss(ch, it.get('explanation', ''))
    if g:
        gloss[ch] = g
    # ～ 组词
    ws = set()
    for m in re.finditer(r'([\u4e00-\u9fff]?)～([\u4e00-\u9fff]?)', it.get('explanation', '')):
        a, b = m.group(1), m.group(2)
        w = (a or '') + ch + (b or '')
        if 2 <= len(w) <= 4:
            ws.add(w)
    ws = [w for w in ws if w != ch and all(c in pin for c in w)]
    if ws:
        words[ch] = ws[:6]

print('gloss', len(gloss), '/', len(all_chars))
print('words', len(words), '/', len(all_chars))

# ---------- 4. 输出 ----------
data = {
    'groups': groups,
    'pin': {c: pin.get(c, ['?']) for c in all_chars},
    'gloss': gloss,
    'words': words,
}
json.dump(data, open('data.json', 'w', encoding='utf-8'), ensure_ascii=False)

# 抽样检查
sample = []
random.seed(7)
for ch in random.sample(all_chars, 40):
    sample.append(f'{ch}\t{pin.get(ch,["?"])[0]}\t{gloss.get(ch,"—")}\t{"、".join(words.get(ch,[])[:3])}')
open('gloss_sample.txt', 'w', encoding='utf-8').write('\n'.join(sample))
print('done')
