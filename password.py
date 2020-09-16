import random

# Generates random password of length pass_length
def generate_pass(pass_length):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit = "1234567890"
    special = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    chars = [lower, upper, digit, special]

    password = ""

    for i in range(pass_length):
        
        index = random.randint(0,3)
        size = len(chars[index]) - 1
        char_index = random.randint(0, size)
        password = password + chars[index][char_index]
        
    return password
