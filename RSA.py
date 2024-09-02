import math
import random

def create_prime(k):
    if k == 1:
        return 2
    while True:
        num = random.randint(10**(k-1), 10**k - 1)
        if check_prime(num):
            return num

def check_prime(num):
    if num % 2 == 0:
        return False
    s = 0
    d = num - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    a = random.randint(2, num - 2)
    x = pow(a, d, num)
    if x == 1 or x == num - 1:
        return True
    for r in range(0, s):
        x = pow(x, 2, num)
        if x == num - 1:
            return True
    return False

def generate_exponent(p, q):  
    while True:
        exponent = random.randint(2, (p-1)*(q-1) - 1)
        if math.gcd(exponent, (p-1)*(q-1)) == 1:
            return exponent

def generate_mod_inverse(exponent, p, q):
    return pow(exponent, -1, (p-1)*(q-1))

def string_to_num(s):
    mapping = {}
    mapping[' '] = 40
    for i in range(26):
        mapping[chr(ord('a') + i)] = 11 + i
    number = 0
    for i in s:
        number *= 100
        number += mapping[i]
    return number

def num_to_string(number):
    reverse_mapping = {}
    for i in range(26):
        reverse_mapping[11+i] = chr(ord('a') + i)
    reverse_mapping[40] = ' '
    text = ""
    while(number != 0):
        text += reverse_mapping[number % 100]
        number = number // 100
    text = text[::-1]
    return text

def perform_encryption(message, exp1, dec2, mod1, mod2):
    return pow(pow(message, exp1, mod1), dec2, mod2)

def perform_decryption(encrypted, dec1, exp2, mod1, mod2):
    encrypted = pow(encrypted, exp2, mod2)
    return pow(encrypted, dec1, mod1)

prime1 = create_prime(10)
prime2 = create_prime(10)
mod1 = prime1 * prime2
Prime1 = create_prime(100)
Prime2 = create_prime(100)
Mod1 = Prime1 * Prime2
prime3 = create_prime(10)
prime4 = create_prime(10)
Prime3 = create_prime(100)
Prime4 = create_prime(100)
mod2 = prime3 * prime4
Mod2 = Prime3 * Prime4
num = 12345678
Num = 987654321
exp1 = generate_exponent(prime1, prime2)
dec1 = generate_mod_inverse(exp1, prime1, prime2)
Exp2 = generate_exponent(Prime4, Prime3)
Dec2 = generate_mod_inverse(Exp2, Prime4, Prime3)
encrypted_num = perform_encryption(num, exp1, Dec2, mod1, Mod2)
decrypted_num = perform_decryption(encrypted_num, dec1, Exp2, mod1, Mod2)
print(decrypted_num)
Exp1 = generate_exponent(Prime1, Prime2)
Dec1 = generate_mod_inverse(Exp1, Prime1, Prime2)
exp2 = generate_exponent(prime3, prime4)
dec2 = generate_mod_inverse(exp2, prime3, prime4)
encrypted_Num = perform_encryption(Num, exp2, Dec1, mod2, Mod1)
decrypted_Num = perform_decryption(encrypted_Num, dec2, Exp1, mod2, Mod1)
print(decrypted_Num)
