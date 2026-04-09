#lệnh chạy: python -m pytest src/test_taxi.py -v
import pytest

def calculate_taxi_fare(distance, seniority, promo_discount):
    if not (1 <= distance <= 1000) or seniority < 0 or not (0 <= promo_discount <= 90):
        return -1

    if distance <= 5:
        base_fare = distance * 12000
    elif distance <= 20:
        base_fare = (5 * 12000) + (distance - 5) * 10000
    else:
        base_fare = (5 * 12000) + (15 * 10000) + (distance - 20) * 9000

    if seniority < 1:
        seniority_rate = 0
    elif 1 <= seniority < 2:
        seniority_rate = 5
    elif 2 <= seniority < 5:
        seniority_rate = 10
    else:
        seniority_rate = 15

    total_discount = min(seniority_rate + promo_discount, 100)
    final_fare = base_fare * (1 - total_discount / 100)
    return int(final_fare)

# --- SINH TEST TỰ ĐỘNG ---

# 1. Test kiểm thử biên (yếu)
@pytest.mark.parametrize("dist, sen, promo, expected", [
    (10, 3, 10, 88000),      # Norm
    (1, 3, 10, 9600),        # Min dist
    (2, 3, 10, 19200),        # Min+ dist
    (999, 3, 10, 7216800),    # Max- dist
    (1000, 3, 10, 7224000),   # Max dist
    (10, 0, 10, 99000),        # Min sen
    (10, 0.1, 10, 99000),      # Min+ sen
    (10, 10, 10, 82500),      # Long sen
    (10, 3, 0, 99000),      # Min promo
    (10, 3, 1, 97900),      # Min+ promo
    (10, 3, 89, 1100),      # Max- promo
    (10, 3, 90, 0),      # Max promo
])
def test_boundary_values(dist, sen, promo, expected):
    assert calculate_taxi_fare(dist, sen, promo) == expected

# 2. Test dựa trên Bảng quyết định (Decision Table)
@pytest.mark.parametrize("dist, sen, promo, expected", [
    (3, 0.5, 0, 36000),
    (30, 6, 20, 195000),
    (15, 1.5, 10, 136000),
    (25, 0.5, 90, 25500),
    (10, 7, 0, 93500),
    (4, 3, 50, 19200),
])
def test_decision_table(dist, sen, promo, expected):
    assert calculate_taxi_fare(dist, sen, promo) == expected

# 3. Kiểm thử dòng điều khiển, độ đo C2.
@pytest.mark.parametrize("dist, sen, promo, expected", [
    (0, 0, 0, -1),
    (5, 1, 0, 57000),
    (15, 1.5, 0, 152000),
    (30, 3, 0, 270000),
    (30, 6, 0, 255000),
])
def test_control_flow(dist, sen, promo, expected):
    assert calculate_taxi_fare(dist, sen, promo) == expected

# 4. Test All_uses coverage
@pytest.mark.parametrize("dist, sen, promo, expected", [
    (0, 1, 10, -1),
    (3, 0, 10, 32400),
    (10, 1.5, 20, 82500),
    (25, 3, 5, 216750),
    (8, 6, 30, 49500),
])
def test_all_uses_coverage(dist, sen, promo, expected):
    assert calculate_taxi_fare(dist, sen, promo) == expected
