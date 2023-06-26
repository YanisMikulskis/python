# треугольник Паскаля
max_l = int(input('Введите начальное число: '))
arr = []
idx = 0
for i in range(max_l):
    idx = 0
    if len(arr) == 0:
        arr.append([len(arr) + 1])
        continue
    else:
        arr_2 = []
        for i in arr[-1]:
            if idx < len(arr[-1]) - 1:
                arr_2.append(arr[-1][idx] + arr[-1][idx + 1])
            idx += 1
            if idx == len(arr[-1]):
                arr_2.insert(0, 1)
                arr_2.insert(len(arr_2), 1)
        arr.append(arr_2)
space_len = len(arr[-1])
space = ' '
for i in arr:
    element = ' '.join(map(lambda x: str(x), i))
    print(f'{space * space_len}{element}')
    space_len -= 1