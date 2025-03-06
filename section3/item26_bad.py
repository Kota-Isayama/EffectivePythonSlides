import pickle


def trace(func):
  def wrapper(*args, **kwargs): # 関数traceの中で関数を定義!
    # 元の関数を呼び出す（中身を書き換えない）
    result = func(*args, **kwargs)  # 可変長位置引数と可変長キーワード引数が活躍！
    print(f"{func.__name__}({args!r}, {kwargs!r})"
      f" -> {result!r}")  # 引数と結果の表示を追加
    return result
  return wrapper  # 新たな関数を定義


@trace
def fibonacci(n):
  """Return the n-th Fibonacci number."""
  if n in (0, 1):
    return n
  else:
    return fibonacci(n - 2) + fibonacci(n - 1)


@trace
def print_deco():
    print("deco!!")


def call_print_deco():
    print_deco()


if __name__ == "__main__":
    print(fibonacci)
    print(fibonacci.__name__)
    print(fibonacci.__dict__)
    print(help(fibonacci))
    pickle.dumps(fibonacci)
