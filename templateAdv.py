# ----------------------------
# テンプレート応用
# エラー回避
# https://docs.python.org/ja/3/tutorial/stdlib2.html?highlight=string%20template#templating
# ----------------------------

from string import Template

print("---- テンプレートの応用 エラー回避 ----")
t = Template('Return the $item to $owner.')
d = dict(item='unladen swallow')
# t.substitute(d)　#KeyError
print(t.safe_substitute(d))
# 'Return the unladen swallow to $owner.'


# ----------------------------
# テンプレート応用
# デリミタの変更
# 使用例 ファイル変更
# ----------------------------
print("---- テンプレートの応用 デリミタの変更 ----")
import time, os.path

photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']


class BatchRename(Template):
    """
    template : 変更前の文書
    delimiter: dictで変更するワードの先頭につけるキーワード
    """

    def __init__(self, template, delimiter='$'):
        super().__init__(template)
        self.delimiter = delimiter


# fmt = input('Enter rename style (%d-date %n-seqnum %f-format):  ')
# Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f
# ここではわざと変更フォーマットを入れる
fmt = "Ashly-%d-%n%f"
t = BatchRename(fmt, '%')
date = time.strftime('%Y%m%d')
for i, filename in enumerate(photofiles):
    # ファイル名,拡張子取得
    base, ext = os.path.splitext(filename)
    newname = t.substitute(d=date, n=i, f=ext)
    print('{0} --> {1}'.format(filename, newname))

# ----------------------------
# さらにテンプレートの応用
# https://stackoverflow.com/questions/1336786/example-of-subclassing-string-template-in-python
# https://docs.python.org/ja/3/library/string.html#string.Template.template
# 通常は$○○で書かれているものを置き換えるが、細かく設定する場合は下記のようにして書くことができる。
# ----------------------------
print("---- テンプレートの応用 デリミタと正規表現----")

from string import Template


class TemplateClone(Template):
    delimiter = '$'
    pattern = r'''
    \$(?:
      (?P<escaped>\$) |   # Escape sequence of two delimiters
      (?P<named>[_a-z][_a-z0-9]*)      |   # delimiter and a Python identifier
      {(?P<braced>[_a-z][_a-z0-9]*)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    '''


class TemplateAlternative(Template):
    delimiter = '[-'
    pattern = r'''
    \[-(?:
       (?P<escaped>-) |            # Expression [-- will become [-
       (?P<named>[^\[\]\n-]+)-\] | # -, [, ], and \n can't be used in names
       \b\B(?P<braced>) |          # Braced names disabled
       (?P<invalid>)               #
    )
    '''


t = TemplateClone("$hi sir")
print(t.substitute({"hi": "hello"}))

# 'hello sir'

ta = TemplateAlternative("[-hi-] sir")
print(ta.substitute({"hi": "have a nice day"}))
# 'have a nice day sir'

ta = TemplateAlternative("[--[-hi-]-]")
print(ta.substitute({"hi": "have a nice day"}))
# '[-have a nice day-]'
