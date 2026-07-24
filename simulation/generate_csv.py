import os
import csv
import random
from datetime import datetime, timedelta

def generate_simulation_data():
    os.makedirs("simulation", exist_ok=True)
    csv_path = os.path.join("simulation", "FITX.csv")

    random.seed(42)
    start_date = datetime(2024, 1, 2)
    end_date = datetime(2024, 1, 31)

    rows = []
    current_date = start_date
    base_price = 17800.0

    while current_date <= end_date:
        # 只生成週一到週五 (0: Mon ... 4: Fri)
        if current_date.weekday() < 5:
            current_time = datetime(current_date.year, current_date.month, current_date.day, 8, 45)
            end_time = datetime(current_date.year, current_date.month, current_date.day, 13, 45)
            
            current_price = base_price + random.gauss(0, 15)
            while current_time <= end_time:
                change = random.gauss(0, 3.5)
                open_p = current_price
                close_p = open_p + change
                high_p = max(open_p, close_p) + abs(random.gauss(0, 2.0))
                low_p = min(open_p, close_p) - abs(random.gauss(0, 2.0))
                volume = int(abs(random.gauss(1200, 300)) + 100)
                open_interest = int(120000 + random.gauss(0, 500))

                rows.append([
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    round(open_p, 1),
                    round(high_p, 1),
                    round(low_p, 1),
                    round(close_p, 1),
                    volume,
                    open_interest
                ])

                current_price = close_p
                current_time += timedelta(minutes=1)

            base_price = current_price

        current_date += timedelta(days=1)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "open", "high", "low", "close", "volume", "open_interest"])
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} bars into {csv_path}")

if __name__ == "__main__":
    generate_simulation_data()
