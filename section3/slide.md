---
marp: true
header: "Effective Python 輪読会 第3回"
footer: 諌山航太
paginate: true
math: mathjax
---

# Effective Python 第3回

---

# 3章　関数

---

## 項目19 複数の戻り値では、4個以上の変数なら決してアンパックしない

Python関数は（タプルを介して）複数の値を返せる。

```Python
def get_stats(number: list[float]):
  minimum = min(numbers)
  maximum = max(numbers)
  return minimum, maximum # カンマで区切ると、タプルになる

numbers = [0, 1, 2, 3]

minimum, maximum = get_stats(numbers) # アンパック代入
```

---

catch-allアンパックで受け取ることもできる。
ワニの体長の列に対して、平均の何％かを計算してソートする関数

```python
def get_avg_ratio(numbers):
  average = sum(numbers) / len(numbers)
  scaled = [ x / average for x in numbers ]
  scaled.sort(reverse=True)
  return scaled

lengths = range(0, 10)
longest, *middle, shortest = get_avg_ratio(lengths)
>>>

```

---

**アンチパターン**
４以上の長さのアンパックを用いて戻り値を受け取る

**推奨パターン**
３以下の長さのアンパックを用いて戻り値を受け取る

**ミスの発生のしやすさ、可読性の観点から**

---

**アンチパターン**
ワニの最大長、最小長、平均長、中央値、母集団のサイズを計算して返す関数

```python
def get_stats(numbers):
  mininum = min(numbers)
  maximum = max(numbers)
  count = len(numbers)
  average = sum(numbers) / count

  sorted_numbers = sorted(numbers)
  median = sorted_numbers[count // 2] # 簡単のため、奇数長のパターンのみ考慮

  return minimum, maximum, average, median, count

minimum, maximum, average, median, count = get_stats(length)
```

---
**問題点**

- 戻り値の順番を間違いやすい（型が同じなので、特定しにくい）
```python
# 正しい
minimum, maximum, average, median, count = get_stats(lengths)
# メディアンと平均が入れ替わっている...
minimum, maximum, median, average, count = get_stats(lengths)
```
- 戻り値を受け取る行が長く、改行を伴いやすい（読みにくい）
```python
minimum, maximum, average, median, count = get_stats(
  lengths)

minimum, maximum, average, median, count =\
  get_stats(lengths)
```

---

**推奨パターン**
- ３要素タプル
- ２変数と１つのアスタリスク付きの式
- もっと短いもの

---

## 項目22 可変長位置引数を使って、見た目をすっきりさせる

**可変長位置引数（スター引数）のメリット**
- 関数呼び出しがより明確になる
- 関数の見た目がよりスッキリする

**可変長位置引数（スター引数）のデメリット**
- 可変長個数の引数が関数に渡される前に常にタプルに変換される
  （ジェネレータオブジェクトを破壊する）
- 全ての呼び出し元を修正しないと、新たな位置引数を追加できない

---

**可変長位置引数とは**
識別子の前に`*`をつけた引数。

```python
def sum(*numbers):
  result = 0
  for number in numbers:  # 可変長の位置引数をリストとして受け取る
    result += number
  return result

result1 = sum(0, 1, 2, 3, 4) # 可変長の位置引数をリストnumbersに渡している
numbers = [5, 6, 7, 8, 9]
result2 = sum(*numbers) # *をつけることで、シーケンスを位置引数として渡せる
print(result1, result2)
>>>
10 35
```

アンパック代入文のアスタリスク付きの式によく似ている。

---

**可変長位置引数のメリット** 可読性
```python
def log(message, values):
  if not values:
    print(message)
  else:
    values_str = ", ".join(str(x) for x in values)
    print(f"{message}: {values_str}")

log("Hi there", [])  # 値のリストを指定しない場合、空リストの指定が必要
```
```python
def log(message, *values):
  if not values:
    print(message)
  else:
    values_str = ", ".join(str(x) for x in values)
    print(f"{message}: {values_str}")

log("Hi there")  # 値を指定しない場合、書かなくて良い。自動でvalues = []となる。
```

---

**可変長位置引数のデメリット**
`*`演算子を使って可変長位置引数を指定すると、強制的にタプルに変換される.
→ ジェネレータオブジェクトが全て展開され、メモリを大量に消費してしまうことも

```python
def my_generator():
  for i in range(10):
    yield i

def my_func(*args):
  print(args)

it = my_generator()
my_func(*it)

>>>
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```

入力個数が少ないことがわかっている場合にのみ可変長位置引数は推奨される

---

**可変長位置引数のデメリット**
全ての呼び出し元を修正しないと関数に対して新たな位置引数を追加できないし、
不具合に気づけない

```python
def log(message: str, *values: list[Any]): # 変更前
  ...

log("Hello", 1, 2) # 古い呼び方
```

```python
def log(sequence: int, message: str, *value: list[Any]): # 変更後
  # sequence: int が先頭に追加された
  ...

log("Hello", 1, 2) # sequence: int = "Hello"になってしまったが、エラーを吐かない！
```
※この現象は可変長位置引数に固有のもの。
 引数が増えて可変長引数の実引数がなくなっても、空リストとして受け取るだけ。

---

## 項目23 キーワード引数にオプションの振る舞いを与える

キーワード引数 := 関数呼び出しの括弧の中で名前への代入式を用いて指定された引数

```python
def remainder(number, divisor):
  return number % divisor

remainder(20, 7)
remainder(20, divisor=7)
remainder(number=20, divisor=7)
remainder(divisor=7, number=20)
# remainder(7, number=20) 位置引数の順番までは変えられない
```

---

### キーワード引数いろいろ

```python
my_kwargs = {
  "number": 20,
  "divisor": 7
}
assert 6 == remainder(**my_kwargs)  # **(辞書)で対応する名前にキーワード引数として渡せる

my_kwargs = {
  "divisor": 7,
}
assert 6 == remainder(number=20, **my_kwargs) # 通常のキーワード引数と**は混在できる

my_kwargs = {
  "number: 20
}
other_kwargs = {
  "divisor": 7
}
assert 6 == remainder(**my_kwargs, **other_kwrags)  # **演算子は複数使える（重複はNG）
```

---

### キーワード引数のメリット３選

1. 初めて読む人にとってわかりやすい ← 自明なのでスキップ
2. デフォルト値を指定できる ← スキップ
3. 後方互換性を保った、引数の拡張ができる

---

#### 3. 後方互換性を保った、引数の拡張ができる

```python
def calc_distance(speed, time):
  """
  Args:
    speed: 時速(km / h)
    time: 時間(h)
  """
  return speed * time


calc_distance(10, 5)  # 50km
```

距離の単位を指定したくなったら...? **キーワード引数が活躍します**

---

```python
def calc_distance(speed, time, unit_per_km=1):
  """
  Args:
    speed: 時速(km / h)
    time: 時間(h)
  """
  return speed * time

calc_distance(10, 5) # 50km
calc_distance(10, 5, unit_per_km=1000)  # 50000m
```

既存の関数呼び出しに影響を与えない！

**特に可変長位置引数を使う関数の後方互換性の確保に重要**

```python
calc_distance(10, 5, 1000)  # 注意:位置で指定すると、オプショナルな引数はわかりにくい
```
---

#### おさらい

```python
def log(message: str, *values: list[Any]): # 変更前
  ...

log("Hello", 1, 2) # 古い呼び方
```

```python
def log(sequence: int, message: str, *value: list[Any]): # 変更後
  # sequence: int が先頭に追加された
  ...

log("Hello", 1, 2) # sequence: int = "Hello"になってしまったが、エラーを吐かない！
```
※この現象は可変長位置引数に固有のもの。
 引数が増えて可変長引数の実引数がなくなっても、空リストとして受け取るだけ。

---

#### 解決策

```python
def log(message: str, *values: list[Any], sequence=0):
  ...

log("Hello", 1) # 元の呼び方 OK
log("Hello", 1, 2, sequence=2) # キーワード引数は*argには入らない!
```

---

## まとめ

---

## 項目24 動的なデフォルト引数をしていするときにはNoneとdocstringを使う

---

動的に値が変わるデフォルト値をキーワード引数に指定したいときがある

例: ロギングメッセージに、時刻を出力したいとき

```python
from time import sleep
from datetime import datetime

# 悪い例
def log(message, when=datetime.now()):
  print(f"{when}: {message}")

log("Hi there!")
sleep(1)
log("Hi again!")

>>>
2025-03-06 14:06:15.120124: Hi there!
2025-03-06 14:06:15.120124: Hi again!
```
あれ？？

---

### なぜか？

`datetime.now()`は関数の定義時に1回評価されるだけだから

```python
from time import sleep
from datetime import datetime

# 悪い例
def log(message, when=datetime.now()): # ← log()の定義時だけよばれたら使い回し
  print(f"{when}: {message}")

log("Hi there!")
sleep(1)
log("Hi again!")

>>>
2025-03-06 14:06:15.120124: Hi there!
2025-03-06 14:06:15.120124: Hi again!
```

---

### どうしたらよい？

デフォルト値を`None`にして、docstringに実際の振る舞いを記述する

```python
# 良い例
def log(message, when=None):
  """Log a message with a timestamp.

  Args:
    message: Message to print.
    when: datetime of when the message occurred.
      Defaults to the present time.  # 実際のデフォルト値
  """
  if when is None:
    when = datetime.now()
  print(f"{when}: {message}")
```

---

### さらに

デフォルト引数がミュータブル（変更可能）なときはさらに重要!!

JSONのデータとして符号化された値をロードする場合

```python
import json

# 悪い例
def decode(data, default={}):  # 全てのdecode呼び出しで{}が共有される
  try:
    return json.loads(data)
  except ValueError:
    return default  # 失敗したら、空の辞書を返したい
```

---

```python
foo = decode("bad data")
foo["stuff"] = 5
bar = decode("also bad")  # ここでも空辞書を返してほしいが...
bar["meep"] = 1
print("foo: ", foo)  # {"stuff": 5}を予想しているが
print("bar: ", bar)  # {"meep": 1}を予想しているが...

>>>
foo: {"stuff": 5, "meep": 1} # barへの変更がfooにも影響している!!
bar: {"stuff": 5, "meep": 1}
```

```
assert foo is bar
```
`foo`も`bar`も同じオブジェクトを参照している

---

`None`をデフォルト引数に指定して、docstringでデフォルトの引数を指定しましょう

```python
import json

# 良い例
def decode(data, default=None):  # デフォルトはNone!
  """Load JSON data from a string.

  Args:
    data: JSON data to decode.
    default: Value to return if decoding fails.
      Defaults to an empty dictionary.  # Noneのとき、空辞書を返す！
  """
  try:
    return json.loads(data)
  except ValueError:
    if default is None:
      default = {}  # 呼び出しのたびに新しいインスタンスを作成
    return default 
```

---

### まとめ

---

## 項目25 キーワード専用引数と位置専用引数で明確さを高める

- 位置専用引数: 位置引数としてしか指定できない
  - `/`より左の引数
  - インターフェース（引数名）を明示したくないものに使用すべし
- キーワード専用引数: キーワード引数としてしか指定できない
  - `*`より右の引数
  - 呼び出し元に引数の明確化を強制したいときに使用すべし
例
```python
def func(a, b, /, c, d, *, e, f):
  ...
```
`a, b`が位置専用引数、`e, f`がキーワード専用引数
`c, d`はどちらでも指定可能（通常の引数がこれ）

---

---

## 項目26 functools.wrapsを使って関数デコレータを定義する

デコレータとは: 関数やクラスの中身を書き換えずに処理を追加するための機能。
  実体は関数を受け取って関数を返す関数。

```python
@trace  # ← @で始まるこれです
def func():
  ...
```

以下と等価
```python
func = trace(func)  # func（関数オブジェクト）を受け取って関数オブジェクトをfuncに再代入
```

---

### デコレータの役立ちタイミング例: 再帰関数のデバッグ

```python
def trace(func):
  def wrapper(*args, **kwargs): # 関数traceの中で関数を定義!
    # 元の関数を呼び出す（中身を書き換えない）
    result = func(*args, **kwargs)  # 可変長位置引数と可変長キーワード引数が活躍！
    print(f"{func.__name__}({args!r}, {kwargs!r})"
      f" -> {result!r}")  # 引数と結果の表示を追加
    return result
  return wrapper  # 新たな関数を定義
```

関数`func`を受け取って関数`wrapper`を返す。

---

### 実際に挙動を見てみよう

フィボナッチ数の計算
$$a_n := a_{n-1} + a_{n-2}\quad (a_0 = 0, a_1 = 1)$$

```python
def fibonacci(n):
  """Return the n-th Fibonacci number."""
  if n in (0, 1):
    return n
  else:
    return fibonacci(n - 2) + fibonacci(n - 1)
```

続きはPyCharmで

---

### 課題: 名前やhelpが崩れる...!
