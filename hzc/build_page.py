# -*- coding: utf-8 -*-
import json, re

chars = json.load(open('chars.json', encoding='utf-8'))
groups = [chars['jia'], chars['yi'], chars['bing']]
all_chars = ''.join(groups)

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

gloss = json.load(open('gloss.json', encoding='utf-8'))

BAD_END = re.compile(r'[也矣焉哉耳]$')
BAD_ANY = re.compile(r'同本义|〈|〉|[（）()]|["“”]|[a-zA-Z]|^同[「『"\'“”]|…|〔〕')


def ok(g):
    if not g:
        return False
    if len(g) < 3 or len(g) > 22:
        return False
    if BAD_END.search(g) or BAD_ANY.search(g):
        return False
    if re.search(r'[～]', g):
        return False
    if g.count('，') >= 1:
        last = g.split('，')[-1]
        if len(last) <= 2:          # 尾随例句残留
            return False
    return True


gl = []
for c in all_chars:
    g = gloss.get(c, '')
    gl.append(g if ok(g) else '')

py = []
py_all = []
for c in all_chars:
    rs = pin.get(c, [])
    py.append(rs[0] if rs else '')
    py_all.append('|'.join(rs[:5]) if len(rs) > 1 else '')

try:
    multi = json.load(open('multi.json', encoding='utf-8'))
except Exception:
    multi = {}

data = {
    'chars': all_chars,
    'py': py,
    'pyAll': py_all,
    'gl': gl,
    'sizes': [4000, 500, 1000],
    'emerg': json.load(open('emergency.json', encoding='utf-8')),
    'multi': multi,
}

print('chars', len(all_chars), 'gloss-ok', sum(1 for x in gl if x), 'poly', sum(1 for x in py_all if x))

tpl = open('template.html', encoding='utf-8').read()
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
marker = 'const DATA = /*__DATA__*/{chars:"",py:[],pyAll:[],gl:[],sizes:[0,0,0]};'
assert marker in tpl, 'marker not found'
out = tpl.replace(marker, 'const DATA = ' + payload + ';')
open('game.html', 'w', encoding='utf-8').write(out)
print('written', len(out))
