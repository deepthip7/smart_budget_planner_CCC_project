# knapsack.py
# Core Dynamic Programming logic for the Smart Budget Planner
# Uses the 0/1 Knapsack algorithm

def knapsack(budget, items):
    n = len(items)
    W = budget
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        item_price = items[i - 1]['price']
        item_value = items[i - 1]['value']

        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]

            if item_price <= w:
                value_if_taken = dp[i - 1][w - item_price] + item_value
                if value_if_taken > dp[i][w]:
                    dp[i][w] = value_if_taken
    selected_items = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1]['price']
    selected_items.reverse()
    return dp[n][W], selected_items, dp
def print_dp_table(dp, items, budget):
    n = len(items)
    print("\n📊 DP Table (rows = items, columns = budget 0 to", budget, ")")
    print("-" * 60)
    header = f"{'Item':<20}" + "".join(f"{w:>4}" for w in range(budget + 1))
    print(header)
    print("-" * len(header))
    row = f"{'(no items)':<20}" + "".join(f"{dp[0][w]:>4}" for w in range(budget + 1))
    print(row)
    for i in range(1, n + 1):
        name = items[i - 1]['name'][:18]
        row = f"{name:<20}" + "".join(f"{dp[i][w]:>4}" for w in range(budget + 1))
        print(row)

    print("-" * len(header))