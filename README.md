# 在线测试

按考试大纲与权威字表整理的逐题自测工具合集。纯前端、无需注册，进度保存在浏览器本地。

**在线地址：<https://entiesci.github.io/OnlineTest/>**

## 已有测试

| 测试 | 地址 | 说明 |
|---|---|---|
| 汉字应用水平测试 · 5500 字通关 | [/hzc/](https://entiesci.github.io/OnlineTest/hzc/) | 依据《汉字应用水平等级及测试大纲》附录 A 字表，甲表 4000 / 乙表 500 / 丙表 1000 逐字测试，另设考前急救 1000 易错字 |

## 目录

```
index.html               测试列表（入口）
robots.txt / sitemap.xml
hzc/
  index.html             本测试的入口页
  game.html              测试主页面（构建产物）
  1000easywrong.html     静态「1000 易错字」页（构建产物）
  template.html          页面模板（含样式与逻辑）
  theme.css              主题变量
  chars.json             甲/乙/丙三个字表
  pinyin.txt             汉字读音数据
  phrase.txt             短语拼音库（多音字例词来源）
  gloss.json             释义数据
  emergency.json         1000 易错字索引
  multi.json             多音字例词表
  build_page.py          生成 game.html
  build_emergency.py     生成易错字表
  build_multi2.py        生成多音字例词表
  build_wrong.py         生成静态易错字页
```

## 新增一个测试

在根目录建一个与 `hzc/` 同级的文件夹（如 `xxx/`），里面放自己的入口页 `index.html`
和测试页，然后在根 `index.html` 的 `.grid` 里加一张卡片指向 `./xxx/`，并把 URL 加进 `sitemap.xml`。

## 重新构建 hzc

```bash
cd hzc
python build_emergency.py   # -> emergency.json
python build_multi2.py      # -> multi.json
python build_page.py        # -> game.html
python build_wrong.py       # -> 1000easywrong.html
```

## 数据说明

- 字表：附录 A 甲表 4000 / 乙表 500 / 丙表 1000，共 5500 字。
- 读音：mozillazg/pinyin-data（多音字取全部读音）。
- 例词：mozillazg/phrase-pinyin-data 短语拼音库，人工表交叉校验后使用。
- 释义：chinese-xinhua 新华字典数据，自动抽取义项。
- 释义题为程序自动抽取，个别释义可能带古义或残缺，仅供参考。

## 许可

仅供学习自测使用。字表、拼音、释义数据版权归原作者及原出版方所有。
