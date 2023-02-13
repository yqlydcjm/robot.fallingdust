
name = "王李张李陈王杨张吴周王刘赵黄吴杨"
new_name = ''
for char in name:
    if char not in new_name:  # 如果不在新的字符串中
        new_name += char  # 拼接到新字符串中的末尾
print(new_name)
