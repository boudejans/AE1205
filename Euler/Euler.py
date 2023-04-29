import math

def ex1():
    sum = 0
    for i in range(1000):
        if i%3 == 0 or i%5 == 0:
            sum = sum + i
    print("Result: " + str(sum))

def ex2():
    sum = 2
    i = 1
    j = 2
    while j < 4000000:
        k = i + j
        if (k % 2) == 0:
            sum += k
        i = j
        j = k
    print("Result: " + str(sum))

def ex3():
    num = 600851475143
    for i in range(1, 1000000):
        if num % i == 0:
            if IsPrime(i):
                result = i
    print("Result: " + str(result))

def IsPrime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

def ex4():
    palindrome = 0
    for i in range (100, 999):
        for j in range (100, 999):
            if i * j > palindrome:
                if str(i*j) == str(i*j)[::-1]:
                    palindrome = i*j
    print("Result: " + str(palindrome))

# Find the smallest possible number that is evenly divisible by numbers from 1 to 20
def ex5():
    result = 0
    i = 1
    while result == 0:
        if DivisionCheck(i):
            result = i
        i += 1
    print("Result: " + str(result))

def DivisionCheck(n):
    for i in range(1, 21):
        if n % i != 0:
            return False
    return True

# Calculate the difference between the square of sum and sum of squares of the first 100 natural numbers
def ex6():
    sumOfSquares = 0
    sum = 0
    for i in range(0, 101):
        sumOfSquares += i**2
        sum += i
    difference = sum**2 - sumOfSquares
    print("Result: " + str(difference))

# Find the 10,001 st prime number
def ex7():
    prime_index = 0
    prime_number = 2
    number = 2
    while prime_index < 10001:
        if IsPrime(number):
            prime_number = number
            prime_index += 1
        number += 1
    print("Result: " + str(prime_number))

# Find the largest product of thirteen digits in the 1000-digit number
def ex8():
    number = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
    largestProduct = 0
    for i in range(0, 1000-13):
        section = number[i:i+13]
        product = 1
        for chr in section:
            product = product * int(chr)
        if product > largestProduct:
            largestProduct = product
    print("Result: " + str(largestProduct))

# Find the pythagorean triplet a + b + c = 1000
def ex9():
    a = 0
    b = 0
    c = 0
    result = 0
    for i in range(0, 400):
        for j in range(0, 400):
            a = i
            b = j
            c = math.sqrt(a**2 + b**2)
            if a + b + c == 1000:
                result = a*b*c
    print("Result: " + str(result))

# Find the sum of all the prime numbers up until 2,000,000
def ex10():
    sum = 0
    for i in range(2, 2000000):
        if IsPrime(i):
            sum += i
        if i % 1000 == 0:
            print(i)

    print("Result: " + str(sum))

def ex54():
    p1_wins = 0
    with open("Poker.txt") as f:
        lines = f.readlines()
        for line in lines:
            p1_hands = line.split(" ")[0:5]
            p2_hands = line.split(" ")[5:10]
            p2_hands[-1] = p2_hands[-1].strip()
            p1_suits = [0] * 4
            p1_numbers = [0] * 13
            p2_suits = [0] * 4
            p2_numbers = [0] * 13
            p1_score = 0
            p2_score = 0
            for card in p1_hands:
                match card[1]:
                    case "C":
                        p1_suits[0] += 1
                    case "S":
                        p1_suits[1] += 1
                    case "H":
                        p1_suits[2] += 1
                    case "D":
                        p1_suits[3] += 1
                for suit in p1_suits:
                    if suit == 4:
                        p1_score = 18
                match card[0].isdigit():
                    case True:
                        p1_numbers[int(card[0])-2] += 1
                    case False:
                        match card[0]:
                            case "J":
                                p1_numbers[9] += 1
                            case "Q":
                                p1_numbers[10] += 1
                            case "K":
                                p1_numbers[11] += 1
                            case "A":
                                p1_numbers[12] += 1
                for number in p1_numbers:
                    if number == 2:
                        p1_score = 14
                    if number == 3:
                        p1_score = 16
                    if number == 4:
                        p1_score = 20

            for card in p2_hands:
                match card[1]:
                    case "C":
                        p2_suits[0] += 1
                    case "S":
                        p2_suits[1] += 1
                    case "H":
                        p2_suits[2] += 1
                    case "D":
                        p2_suits[3] += 1
                for suit in p2_suits:
                    if suit == 4:
                        p1_score = 18
                match card[0].isdigit():
                    case True:
                        p2_numbers[int(card[0])-2] += 1
                    case False:
                        match card[0]:
                            case "J":
                                p2_numbers[9] += 1
                            case "Q":
                                p2_numbers[10] += 1
                            case "K":
                                p2_numbers[11] += 1
                            case "A":
                                p2_numbers[12] += 1
                for number in p2_numbers:
                    if number == 2:
                        p2_score = 14
                    if number == 3:
                        p2_score = 16
                    if number == 4:
                        p2_score = 20

            if p1_score > p2_score:
                p1_wins += 1
    print("Result: " + str(p1_wins))


ex54()
