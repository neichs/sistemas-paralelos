from time import time
import numpy as np

def sum_elements(v):
  res = 0
  for e in v:
    res += e
  return res


if __name__ == '__main__':
  c = 100000000
  arr = np.random.rand(c)
  init = time()
  result = sum_elements(arr)
  end = time() - init
  print("Result:", result, "Time:", end, "With C =", c)