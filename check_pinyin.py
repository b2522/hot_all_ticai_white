from pypinyin import lazy_pinyin, Style

# 测试问题题材的拼音首字母
plates_to_check = ["股权转让", "IP经济/谷子经济", "大消费"]

for plate in plates_to_check:
    pinyin_initial = ''.join(lazy_pinyin(plate, style=Style.FIRST_LETTER))
    print(f"题材: {plate} -> 拼音首字母: {pinyin_initial}")
    print(f"'dxf' 是否等于首字母: {'dxf' == pinyin_initial.lower()}")
    print(f"首字母是否以'dxf'开头: {pinyin_initial.lower().startswith('dxf')}")
    print()
