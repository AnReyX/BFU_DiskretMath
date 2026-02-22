def solve_grid_tasks():
    width = 21
    height = 18

    dp = [[0 for _ in range(height + 1)] for _ in range(width + 1)]

    dp[0][0] = 1

    for x in range(width + 1):
        for y in range(height + 1):
            if x == 0 and y == 0:
                continue

            ways_from_left = dp[x - 1][y] if x > 0 else 0
            ways_from_bottom = dp[x][y - 1] if y > 0 else 0

            dp[x][y] = ways_from_left + ways_from_bottom

    answer_1 = dp[width][height]

    dp2 = [[[0, 0] for _ in range(height + 1)] for _ in range(width + 1)]

    if width >= 1:
        dp2[1][0][0] = 1

    if height >= 1:
        dp2[0][1][1] = 1

    for x in range(width + 1):
        for y in range(height + 1):
            if (x == 0 and y == 0) or (x == 1 and y == 0) or (x == 0 and y == 1):
                continue

            if x > 0:
                dp2[x][y][0] = dp2[x - 1][y][0] + dp2[x - 1][y][1]

            if y > 0:
                dp2[x][y][1] = dp2[x][y - 1][0]

    answer_2 = dp2[width][height][0] + dp2[width][height][1]

    return answer_1, answer_2


ans1, ans2 = solve_grid_tasks()
print(f"Задача 1 (все пути): {ans1}")
print(f"Задача 2 (без двойных вертикальных): {ans2}")