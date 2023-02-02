from cs50 import get_float

coins = 0

while True:
    input = get_float("Change owed:")
    if input > 0.0 :
        break

convert = round(int(input * 100))

coins += convert // 25 #quarters
convert %= 25
coins += convert // 10 # dimes
convert %= 10
coins += convert // 5 # nickles
convert %= 5
coins += convert //1 # pennies

print(coins)