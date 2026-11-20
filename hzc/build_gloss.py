# -*- coding: utf-8 -*-
import json, re, random

chars = json.load(open('chars.json', encoding='utf-8'))
groups = {k: chars[k] for k in ['jia', 'yi', 'bing']}
all_chars = groups['jia'] + groups['yi'] + groups['bing']

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

dic = {}
for it in json.load(open('xinhua_word.json', encoding='utf-8')):
    w = it.get('word', '')
    if w and len(w) == 1:
        dic[w] = it

BAD = re.compile(r'形声|会意|象形|同本义|本义|又如|〈|〉|\(|\)|"|“|”|《|》|--')
SENSE = re.compile(r'[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑]')


def clean(g):
    if '～' in g:
        g = g.split('～')[0]
    for sep in ['。', '；', ';', '！', '？']:
        g = g.split(sep)[0]
    g = g.strip(' ，、：:,')
    g = re.sub(r'^[，、,。；;：:\s]+', '', g)
    g = g.strip(' ，、：:,')
    if len(g) < 3 or len(g) > 22:
        return None
    if BAD.search(g):
        return None
    if re.search(r'[a-zA-Z0-9]', g):
        return None
    if g.count('，') > 1:
        return None
    return g


def extract(ch, text):
    t = text.replace('\r', '')
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    # 1) 行内以义项符号开头
    for l in lines:
        m = SENSE.search(l)
        if not m:
            continue
        head = l[:m.start()]
        if head and not (head.startswith(ch) or re.search(r'[a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]', head)):
            continue
        if head and BAD.search(head.replace(ch, '')):
            continue
        parts = SENSE.split(l)
        for seg in parts[1:]:
            g = clean(seg)
            if g:
                return g
    # 2) 退化：普通释义行
    for l in lines:
        if len(l) > 60:
            continue
        if l.startswith(ch) and len(l) > 3:
            g = clean(l[1:].lstrip('，、 '))
            if g:
                return g
    return None


gloss = {}
for ch in all_chars:
    it = dic.get(ch)
    if not it:
        continue
    g = extract(ch, it.get('explanation', ''))
    if g:
        gloss[ch] = g

print('gloss', len(gloss), '/', len(all_chars))
random.seed(11)
sample = [f'{c}\t{gloss.get(c,"—")}' for c in random.sample(all_chars, 60)]
open('gloss_sample2.txt', 'w', encoding='utf-8').write('\n'.join(sample))
json.dump(gloss, open('gloss.json', 'w', encoding='utf-8'), ensure_ascii=False)
