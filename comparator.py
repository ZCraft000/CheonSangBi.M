import math

def total_probability(p1, p2, p3, total_draws=10, sum_target=20, verbose=False):
    """
    Returns the total probability of reaching `sum_target` in at most `total_draws`
    draws, where each draw adds +1 with p1, +2 with p2, +3 with p3.
    """
    total = 0.0
    combos = []
    i = 1

    # x = count of +3, y = count of +2, z = count of +1 (z solved from equation)
    max_x = min(total_draws, sum_target // 3)
    for x in range(0, max_x + 1):
        max_y = min(total_draws - x, (sum_target - 3*x) // 2)  # ensure z >= 0
        for y in range(0, max_y + 1):
            z = sum_target - 3*x - 2*y
            if z < 0:
                continue
            n = x + y + z
            if n > total_draws:
                continue

            # multinomial coefficient * product of probabilities
            coeff = math.factorial(n) // (math.factorial(x) * math.factorial(y) * math.factorial(z))
            prob = coeff * (p3 ** x) * (p2 ** y) * (p1 ** z)
            total += prob
            combos.append((x, y, z, n, coeff, prob))

            if verbose:
                print(f"{i}. 3*{x} + 2*{y} + 1*{z} (n={n}, coeff={coeff}) => probability = {prob:.7f}")
                i += 1

    return total, combos

# ----- Old and new settings -----
old = dict(p1=0.676, p2=0.259, p3=0.065)
new = dict(p1=0.64, p2=0.28, p3=0.08)

# Compute totals (set verbose=True if you want to list each combination)
total_old, combos_old = total_probability(**old, total_draws=10, sum_target=20, verbose=False)
total_new, combos_new = total_probability(**new, total_draws=10, sum_target=20, verbose=False)

print(f"total_probability_old = {total_old:.7f}")
print(f"total_probability_new = {total_new:.7f}")
print(f"difference (new - old) = {total_new - total_old:.7f}")

# (Optional) sanity check: both should consider the same number of valid (x,y,z) combos
print(f"# of valid combos = {len(combos_old)} (old), {len(combos_new)} (new)")
