---
marp: true
header: "Effective Python 輪読会 第3回"
footer: 諌山航太
paginate: true
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
