import math

# Define probabilities for outcomes:
p1 = 0.62  # probability for outcome 1 (經脈打通+1)
p2 = 0.29  # probability for outcome 2 (經脈打通+2)
p3 = 0.09  # probability for outcome 3 (經脈打通+3)
total_draws = 10  # maximum number of draws 總共可以打通次數
sum_target = 20  # target sum to reach 目標打通經脈總和
total_probability = 0.0
solutions = []
i=1
# Iterate over possible counts for x, y, z.
# We set an upper bound (0 to 10) since the total number of draws cannot exceed 10.
for x in range(0, 11):
    for y in range(0, 11):
        for z in range(0, 11):
            # Check both the sum constraint and the equation constraint.
            if x + y + z <= total_draws and (3*x + 2*y + z == sum_target):
                n = x + y + z  # total number of draws
                # Calculate the multinomial coefficient:
                coeff = math.factorial(n) // (math.factorial(x) * math.factorial(y) * math.factorial(z))
                # Calculate the probability for this combination:
                prob = coeff * (p3 ** x) * (p2 ** y) * (p1 ** z)
                total_probability += prob
                solutions.append((x, y, z, n, coeff, prob))
                if i < 10:
                    print(f"{i}. ", f"3*{x} + 2*{y} + 1*{z} (n={n}, coeff={coeff}) => probability = {prob:.7f}")
                else:
                    print(f"{i}.", f"3*{x} + 2*{y} + 1*{z} (n={n}, coeff={coeff}) => probability = {prob:.7f}")
                i+=1

print(f"\nTotal probability of reaching sum {sum_target} in at most {total_draws} draws: {total_probability:.7f}")