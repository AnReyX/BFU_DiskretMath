# Лабораторная работа №5. Вариант 27
# n = 31, m = 21, r = 10
# g(x) = 11101101001

n = 31
m = 21
r = n - m
g_x = "11101101001"


def xor_strings(s1, s2): # Побитовое XOR
    return "".join('0' if a == b else '1' for a, b in zip(s1, s2))


def poly_div_mod2(dividend, divisor): # Деление многочленов по модулю 2

    divisor = divisor.lstrip('0')
    if not divisor: return "0" * r

    temp = list(dividend)

    for i in range(len(dividend) - len(divisor) + 1):
        if temp[i] == '1':  # Если текущий бит 1, делаем XOR с делителем
            for j in range(len(divisor)):
                temp[i + j] = '0' if temp[i + j] == divisor[j] else '1'

    remainder = "".join(temp)[-r:] # берем последние r бит - остаток
    return remainder


def hamming_distance(s1, s2): # Расстояние Хэмминга
    return sum(1 for a, b in zip(s1, s2) if a != b)


G_sys = [] # Порождающая матрица
for i in range(m):
    # Формируем строку единичной матрицы
    info_bits = ['0'] * m
    info_bits[i] = '1'
    info_str = "".join(info_bits)

    # Сдвигаем на r разрядов
    shifted_info = info_str + "0" * r

    # Находим остаток от деления на порождающий многочлен
    remainder = poly_div_mod2(shifted_info, g_x)

    # Кодовое слово для матрицы = инфо_биты + остаток
    G_sys.append(info_str + remainder)

print("- - - 1. Порождающая матрица (21x31) - - -")
for i in range(m):
    print(f"Строка {i + 1:2}: {G_sys[i][:m]} | {G_sys[i][m:]}")


cw1 = "0" * n  # Нулевое слово
cw2 = G_sys[m - 1]  # Последняя строка матрицы (инфо: 00..01)
cw3 = G_sys[0]  # Первая строка матрицы (инфо: 10..00)

# Слово 4: Сумма (XOR) первой и последней строк
cw4_info = "1" + "0" * (m - 2) + "1"
cw4_rem = xor_strings(G_sys[0][m:], G_sys[m - 1][m:])
cw4 = cw4_info + cw4_rem

codewords_fragment = [cw1, cw2, cw3, cw4]

print("- - - 2. Фрагмент множества кодовых слов - - -")
print(f"V1 (инфо: все 0): {cw1}")
print(f"V2 (инфо: 21-я ): {cw2} (Вес: {cw2.count("1")})")
print(f"V3 (инфо: 1-я  ): {cw3} (Вес: {cw3.count("1")})")
print(f"V4 (сумма 1 и 21): {cw4} (Вес: {cw4.count("1")})")
print()

d_min = 5
t_obn = d_min - 1
t_ispr = (d_min - 1) // 2

print("- - - 3. Характеристики кода - - -")
print(f"Минимальное кодовое расстояние d_min = {d_min}")
print(f"Кратность гарантированно обнаруживаемых ошибок (t_обн) = {t_obn}")
print(f"Кратность гарантированно исправляемых ошибок (t_испр) = {t_ispr}")
print()


print("- - - 4. Фрагмент таблицы кодовых расстояний - - -")
print("    | V1 | V2 | V3 | V4 |")
print("----|----|----|----|----|")
for i, cw_A in enumerate(codewords_fragment):
    row_dists = []
    for cw_B in codewords_fragment:
        dist = hamming_distance(cw_A, cw_B)
        row_dists.append(f"{dist:2}")
    print(f" V{i + 1} | " + " | ".join(row_dists) + " |")
print()


print("- - - 5. Примеры, иллюстрирующие свойства кода - - -")
original_word = cw2
print(f"Отправлено слово:    {original_word}")

# А) Ошибка, которую код ИСПРАВИТ (кратность 2)
# Инвертируем последние 2 бита
err_2_bits = list(original_word)
err_2_bits[-1] = '0' if err_2_bits[-1] == '1' else '1'
err_2_bits[-2] = '0' if err_2_bits[-2] == '1' else '1'
received_2_err = "".join(err_2_bits)
syndrome_2_err = poly_div_mod2(received_2_err, g_x)

print(f"\nА) Исправление (2 ошибки в конце):")
print(f"Принято искаженное:  {received_2_err}")
print(f"Делим на g(x), синдром (остаток): {syndrome_2_err}")
print(
    "Вывод: Синдром НЕ нулевой, ошибка обнаружена. Т.к. ошибок 2 (<= t_испр), синдром однозначно укажет декодеру на эти два бита, и код их исправит.")

# Б) Ошибка, которую код ОБНАРУЖИТ, НО НЕ ИСПРАВИТ (задание 4 - кратность 3)
# Инвертируем последние 3 бита (это и есть требуемый вектор ошибки)
err_3_bits = list(original_word)
err_3_bits[-1] = '0' if err_3_bits[-1] == '1' else '1'
err_3_bits[-2] = '0' if err_3_bits[-2] == '1' else '1'
err_3_bits[-3] = '0' if err_3_bits[-3] == '1' else '1'
received_3_err = "".join(err_3_bits)
syndrome_3_err = poly_div_mod2(received_3_err, g_x)

vector_e = "0" * (n - 3) + "111"

print(f"\nБ) Обнаружение без возможности исправления (Вектор ошибки: {vector_e}):")
print(f"Принято искаженное:  {received_3_err}")
print(f"Делим на g(x), синдром (остаток): {syndrome_3_err}")
print(
    "Вывод: Синдром НЕ нулевой, код понял, что данные сломаны. Но т.к. ошибок 3 (> t_испр), этот синдром совпадет с синдромом от какой-то другой ошибки кратности 1 или 2. Код исправит не те биты (ошибочное декодирование).")