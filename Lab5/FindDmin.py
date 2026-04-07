import time


def poly_div_mod2(dividend_str, divisor_str):
    divisor = divisor_str.lstrip('0')
    r = 10
    if not divisor: return "0" * r
    temp = list(dividend_str)
    for i in range(len(dividend_str) - len(divisor) + 1):
        if temp[i] == '1':
            for j in range(len(divisor)):
                temp[i + j] = '0' if temp[i + j] == divisor[j] else '1'
    return "".join(temp)[-r:]


print("Подсчёт d_min:")
n = 31
k = 21
r = 10
g_x = "11101101001"

# Строим строки матрицы G в целых числах для возможности операции побитового XOR ^
G_matrix_ints = []
for i in range(k):
    info_bits = ['0'] * k
    info_bits[i] = '1'
    shifted_info = "".join(info_bits) + "0" * r
    rem = poly_div_mod2(shifted_info, g_x)
    codeword_str = "".join(info_bits) + rem

    G_matrix_ints.append(int(codeword_str, 2))

total_words = (1 << k) - 1  # 2^21 - 1 = 2097151 (без нулевого слова)
min_weight = n + 1
best_codeword_int = 0
best_info_int = 0

start_time = time.time()

# Шаг 2: Полный перебор всех возможных информационных векторов
for info_val in range(1, total_words + 1):
    codeword_val = 0
    temp_info = info_val
    row_index = k - 1

    # Умножение вектора на матрицу сведено к битовым операциям XOR
    while temp_info > 0:
        if temp_info & 1:  # Если младший бит равен 1
            codeword_val ^= G_matrix_ints[row_index]  # Прибавляем строку матрицы
        temp_info >>= 1  # Сдвигаем на следующий бит
        row_index -= 1

    # Считаем количество единиц в полученном кодовом слове
    # bin().count('1') работает очень быстро на уровне Си внутри Python
    weight = bin(codeword_val).count('1')

    if weight < min_weight:
        min_weight = weight
        best_codeword_int = codeword_val
        best_info_int = info_val

end_time = time.time()

print("-" * 50)
print(f"ГОТОВО! Время выполнения: {end_time - start_time:.2f} сек.")
print(f"Минимальное количество единиц (кодовое расстояние) d_min = {min_weight}")

# Переводим найденное число обратно в двоичную строку с нулями слева
info_str = bin(best_info_int)[2:].zfill(k)
cw_str = bin(best_codeword_int)[2:].zfill(n)

print("\nДоказательство (первое найденное слово с таким весом):")
print(f"Информационный вектор: {info_str}")
print(f"Кодовое слово (31 бит): {cw_str}")
print(f"Проверка: единиц в слове действительно {cw_str.count('1')}")
print("-" * 50)