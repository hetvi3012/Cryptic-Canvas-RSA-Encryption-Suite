from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

def create_prime(k):
    """Generates a prime number with k digits."""
    if k == 1:
        return 2
    while True:
        num = random.randint(10**(k-1), 10**k - 1)
        if check_prime(num):
            return num

def check_prime(num):
    """Uses Miller-Rabin primality test to check if a number is prime."""
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
    """Generates the public exponent."""
    while True:
        exponent = random.randint(2, (p-1)*(q-1) - 1)
        if math.gcd(exponent, (p-1)*(q-1)) == 1:
            return exponent

def generate_mod_inverse(exponent, p, q):
    """Generates the private exponent using modular inverse."""
    return pow(exponent, -1, (p-1)*(q-1))

def string_to_num(s):
    """Converts a string to a number using a simple encoding."""
    mapping = {' ': 0}  # Space at 0
    for i in range(10):
        mapping[str(i)] = 1 + i  # Numbers 0-9 from 1 to 10
    for i in range(26):
        mapping[chr(ord('a') + i)] = 11 + i  # Lowercase letters from 11 to 36
        mapping[chr(ord('A') + i)] = 37 + i  # Uppercase letters from 37 to 62

    number = 0
    for char in s:
        number *= 100  # Shift digits over
        number += mapping[char]  # Add the mapped value
    return number



def num_to_string(number):
    """Converts a number back to a string using a simple decoding."""
    reverse_mapping = {0: ' '}  # Space mapped to 0
    for i in range(10):
        reverse_mapping[1 + i] = str(i)  # Mapping for numbers 0-9
    for i in range(26):
        reverse_mapping[11 + i] = chr(ord('a') + i)  # Mapping for lowercase
        reverse_mapping[37 + i] = chr(ord('A') + i)  # Mapping for uppercase

    text = ""
    while number != 0:
        text += reverse_mapping[number % 100]
        number //= 100
    return text[::-1]



def perform_encryption(message, exp1, dec2, mod1, mod2):
    """Performs the encryption using the custom logic."""
    return pow(pow(message, exp1, mod1), dec2, mod2)

def perform_decryption(encrypted, dec1, exp2, mod1, mod2):
    """Performs the decryption using the custom logic."""
    encrypted = pow(encrypted, exp2, mod2)
    return pow(encrypted, dec1, mod1)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/generate-keys', methods=['GET'])
def generate_keys():
    """Generates RSA keys with custom logic."""
    # First set of primes
    prime1 = create_prime(10)
    prime2 = create_prime(10)
    mod1 = prime1 * prime2
    
    # Second set of primes
    prime3 = create_prime(10)
    prime4 = create_prime(10)
    mod2 = prime3 * prime4

    # Large primes for second level encryption
    Prime1 = create_prime(100)
    Prime2 = create_prime(100)
    Mod1 = Prime1 * Prime2

    Prime3 = create_prime(100)
    Prime4 = create_prime(100)
    Mod2 = Prime3 * Prime4

    # Exponents and inverses
    exp1 = generate_exponent(prime1, prime2)
    dec1 = generate_mod_inverse(exp1, prime1, prime2)
    
    Exp2 = generate_exponent(Prime4, Prime3)
    Dec2 = generate_mod_inverse(Exp2, Prime4, Prime3)
    
    exp2 = generate_exponent(prime3, prime4)
    dec2 = generate_mod_inverse(exp2, prime3, prime4)

    Exp1 = generate_exponent(Prime1, Prime2)
    Dec1 = generate_mod_inverse(Exp1, Prime1, Prime2)

    return jsonify({
        'public_key_1': (str(exp1), str(mod1)),
        'private_key_1': (str(dec1), str(mod1)),
        'public_key_2': (str(Exp2), str(Mod2)),
        'private_key_2': (str(Dec2), str(Mod2)),
        'public_key_3': (str(exp2), str(mod2)),
        'private_key_3': (str(dec2), str(mod2)),
        'public_key_4': (str(Exp1), str(Mod1)),
        'private_key_4': (str(Dec1), str(Mod1))
    })

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypts a provided message using the custom keys."""
    message = request.form['message']
    exp1_str, mod1_str = request.form['public_key_1'].split(',')
    Dec2_str, Mod2_str = request.form['private_key_2'].split(',')

    exp1 = int(exp1_str)
    mod1 = int(mod1_str)
    Dec2 = int(Dec2_str)
    Mod2 = int(Mod2_str)
    
    encrypted_message = perform_encryption(string_to_num(message), exp1, Dec2, mod1, Mod2)
    return jsonify(encrypted_message=str(encrypted_message))

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypts a provided message using the custom keys."""
    encrypted_message = int(request.form['encrypted_message'])
    dec1_str, mod1_str = request.form['private_key_1'].split(',')
    Exp2_str, Mod2_str = request.form['public_key_2'].split(',')

    dec1 = int(dec1_str)
    mod1 = int(mod1_str)
    Exp2 = int(Exp2_str)
    Mod2 = int(Mod2_str)
    
    decrypted_message = perform_decryption(encrypted_message, dec1, Exp2, mod1, Mod2)
    return jsonify(decrypted_message=num_to_string(decrypted_message))

if __name__ == '__main__':
    app.run(debug=True)
