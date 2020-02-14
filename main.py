from string import Template

# 文章(ファイルから文書を読み込み)
s = "Hi $name. $contents Have a good day"

# 置き換え
context = {
    "name": "Mike",
    "contents": "How are you?"
}

# 文書の置き換え
t = Template(s)
contents = t.substitute(context)
print(contents)