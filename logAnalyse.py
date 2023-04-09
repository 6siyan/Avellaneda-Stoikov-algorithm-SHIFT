import matplotlib.pyplot as plt

# Load logs from file
with open('trading_logs.txt', 'r') as f:
    logs = f.read().splitlines()[1:]

# Initialize variables for P&L calculation
positions = {}
total_pnl = 0
pnl_history = []

# Calculate P&L for each trade and update positions
for log in logs:
    log = log.split(', ')
    ticker = log[0].split(': ')[1]
    action = log[1].split(': ')[1]
    price = float(log[2].split(': ')[1])
    if action == 'Type.MARKET_BUY':
        if ticker in positions:
            positions[ticker] += 1
        else:
            positions[ticker] = 1
    elif action == 'Type.MARKET_SELL':
        if ticker in positions:
            pnl = (price - positions[ticker] * positions[ticker]) * positions[ticker]
            total_pnl += pnl
            pnl_history.append(total_pnl)
            del positions[ticker]

# Plot P&L over time and price
plt.plot(pnl_history)
plt.title('Profit and Loss over Time')
plt.xlabel('Trade')
plt.ylabel('Profit and Loss')
plt.savefig('pnl_over_time.png')
plt.clf()

prices = {}
for log in logs:
    log = log.split(', ')
    ticker = log[0].split(': ')[1]
    price = float(log[2].split(': ')[1])
    if ticker in prices:
        prices[ticker].append(price)
    else:
        prices[ticker] = [price]

for ticker in prices:
    plt.plot(prices[ticker], label=ticker)

plt.title('Price over Time')
plt.xlabel('Trade')
plt.ylabel('Price')
plt.legend()
plt.savefig('price_over_time.png')