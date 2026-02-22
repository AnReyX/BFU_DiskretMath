def solve_abrakadabra():
    letters_count = {
        'А': 5,
        'Б': 2,
        'Р': 2,
        'К': 1,
        'Д': 1
    }

    target_length = 6

    total_words = 0

    def build_word(current_length):
        nonlocal total_words

        if current_length == target_length:
            total_words += 1
            return

        for char in letters_count:
            if letters_count[char] > 0:
                letters_count[char] -= 1

                build_word(current_length + 1)

                letters_count[char] += 1

    build_word(0)

    return total_words


result = solve_abrakadabra()
print(f"Количество различных слов длины 6: {result}")