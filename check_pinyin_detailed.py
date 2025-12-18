from pypinyin import lazy_pinyin, Style

# 详细测试问题题材的拼音首字母生成
plates_to_check = ["股权转让", "IP经济/谷子经济", "大消费"]
user_input = "dxf"

print(f"用户输入: {user_input}")
print()

for plate in plates_to_check:
    print(f"题材: {plate}")
    print(f"直接匹配: '{user_input}' 是否在 '{plate.lower()}' 中: {user_input in plate.lower()}")
    
    # 测试完整的题材字符串（模拟实际情况）
    full_plate_string = "股权转让、IP经济/谷子经济"
    print(f"完整题材字符串: {full_plate_string}")
    print(f"直接匹配(完整字符串): '{user_input}' 是否在 '{full_plate_string.lower()}' 中: {user_input in full_plate_string.lower()}")
    
    # 测试拼音首字母
    pinyin_initial = ''.join(lazy_pinyin(plate, style=Style.FIRST_LETTER))
    print(f"拼音首字母: {pinyin_initial}")
    print(f"拼音首字母(小写): {pinyin_initial.lower()}")
    print(f"拼音首字母匹配: '{user_input}' 是否等于 '{pinyin_initial.lower()}': {user_input == pinyin_initial.lower()}")
    print(f"首字母是否以 '{user_input}' 开头: {pinyin_initial.lower().startswith(user_input)}")
    
    # 检查拆分后的每个部分
    if '、' in plate:
        print(f"\n拆分后的题材:")
        for p in plate.split('、'):
            pinyin_part = ''.join(lazy_pinyin(p, style=Style.FIRST_LETTER))
            print(f"  - {p} -> {pinyin_part} -> 与 '{user_input}' 匹配: {user_input in pinyin_part.lower()}")
    
    print()
