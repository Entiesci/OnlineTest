# -*- coding: utf-8 -*-
"""用「短语拼音库」给多音字配例词（每个读音一个词），人工表优先。"""
import json, re
from multi_curated import M as CURATED

chars = json.load(open('chars.json', encoding='utf-8'))
allc = chars['jia'] + chars['yi'] + chars['bing']
in_set = set(allc)

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

TONE = 'āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜüêńňǹ'
def strip_tone(s):
    return ''.join(c for c in s if c not in TONE)

def norm_reading(ch, r):
    rs = pin.get(ch, [])
    if r in rs:
        return r
    cand = [x for x in rs if strip_tone(x) == strip_tone(r)]
    return cand[0] if len(cand) == 1 else None

# 收集候选：字 -> 读音 -> [(词, 长度)]
cand = {}
phrase_read = {}          # 词 -> {字: 读音}，用于校验人工表
lines = open('phrase.txt', encoding='utf-8').read().split('\n')
for line in lines:
    if not line or line.startswith('#'):
        continue
    if ': ' not in line:
        continue
    w, p = line.split(': ', 1)
    w = w.strip()
    syl = p.split()
    cs = list(w)
    if len(cs) != len(syl):
        continue
    for i, c in enumerate(cs):
        r = norm_reading(c, syl[i])
        if r:
            phrase_read.setdefault(w, {})[c] = r
    if len(w) < 2 or len(w) > 4:
        continue
    allin = all(c in in_set for c in cs)
    for i, c in enumerate(cs):
        if len(pin.get(c, [])) < 2:
            continue
        r = norm_reading(c, syl[i])
        if not r:
            continue
        cand.setdefault(c, {}).setdefault(r, []).append((w, 0 if allin else 1))

def best(ws):
    ws = sorted(set(ws), key=lambda t: (t[1], len(t[0]), t[0]))
    return ws[0][0] if ws else None

multi = {}
for ch, byr in cand.items():
    pairs = []
    for r, ws in byr.items():
        b = best(ws)
        if b:
            pairs.append([b, r])
    if len(pairs) >= 1:
        multi[ch] = pairs

print('短语库覆盖多音字:', len(multi))

# 人工表覆盖（质量更高），但用短语库交叉校验读音
for ch, pairs in CURATED.items():
    if ch not in in_set:
        continue
    ok = []
    for w, r in pairs:
        if ch not in w or len(w) < 2 or len(w) > 4:
            continue
        if any(c not in in_set for c in w):
            continue
        nr = norm_reading(ch, r)
        # 必须能被短语库验证，否则丢弃（避免人工笔误）
        pr = phrase_read.get(w, {}).get(ch)
        if not pr:
            continue
        nr = pr
        if nr and not any(x[1] == nr for x in ok):
            ok.append([w, nr])
    if len(ok) >= 1:
        multi[ch] = ok

print('合计:', len(multi))
json.dump(multi, open('multi.json', 'w', encoding='utf-8'), ensure_ascii=False)
for ch in '差行长重处塞着得为':
    if ch in multi:
        print(ch, multi[ch])
