def solve():
    t = int(input().strip())
    out_lines = []

    for _ in range(t):
        n = int(input().strip())
        s = input().strip()

        # prefix[i] = az első i szegmensben (s[0..i-1]) levő '1'-ek száma
        prefix = [0] * (n + 1)
        for i in range(1, n + 1):
            prefix[i] = prefix[i - 1] + (1 if s[i - 1] == '1' else 0)

        # tomb[i] = max eladható hossz az első i szegmensből
        tomb = [0] * (n + 1)

        for i in range(1, n + 1):
            # alap: nem használjuk az i. szegmenst új darab részeként
            tomb[i] = tomb[i - 1]

            # próbáljuk az i-ben végződő összes szakaszt
            for j in range(1, i + 1):
                ones = prefix[i] - prefix[j - 1]
                length = i - j + 1
                # eladható, ha több az 1, mint a 0
                if 2 * ones > length:
                    tomb[i] = max(tomb[i], tomb[j - 1] + length)

        out_lines.append(str(tomb[n]))

    print("\n".join(out_lines))


if __name__ == "__main__":
    solve()
