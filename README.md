# 汉字应用水平测试 · 5500 字通关

依据教育部、国家语委《汉字应用水平等级及测试大纲》附录 A《汉字应用水平测试字表》制作的在线测试工具。
纯前端单页，无需注册，进度保存在浏览器本地。

**在线地址：<https://entiesci.github.io/OnlineTest/hzc/>**

## 内容

- **5500 字逐字测试**：甲表 4000 字 → 乙表 500 字 → 丙表 1000 字，组内随机打乱；每个字一题，考读音或释义。
- **多音字按例词考**：给出例词（如「擂台」「银行」「差不多」），问词中那个字的读音，选项是该字自己的不同读音。
- **考前急救 1000 易错字**：形近易混 225 + 多音易读 261 + 生僻易忘 514，独立一关。
- **三档自评**：不熟 / 会认不会写 / 掌握；每 100 字给出统计（掌握率、用时、节奏、预计剩余）。
- **辅助操作**：撤销上一步（Z）、改判上一题（U）、查看上一题（V）、看答案（空格）。
- **导出**：结束时导出「不熟字」「会认不会写」字表。
- 浅色/深色两套主题，手机可用。

## 目录

```
index.html              入口页
robots.txt / sitemap.xml
hzc/
  index.html            测试主页面（构建产物）
  1000easywrong.html    静态「1000 易错字」页（构建产物）
  template.html         页面模板（含样式与逻辑）
  theme.css             主题变量
  chars.json            甲/乙/丙三个字表
  pinyin.txt            汉字读音数据
  phrase.txt            短语拼音库（多音字例词来源）
  gloss.json            释义数据
  emergency.json        1000 易错字索引
  multi.json            多音字例词表
  build_page.py         生成测试页
  build_emergency.py    生成易错字表
  build_multi2.py       生成多音字例词表
  build_wrong.py        生成静态易错字页
```

## 重新构建

```bash
cd hzc
python build_emergency.py   # -> emergency.json
python build_multi2.py      # -> multi.json
python build_page.py        # -> index.html（测试页）
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
