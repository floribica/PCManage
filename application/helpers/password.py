import random


def generate_password():
    password_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$^&()_+"
    password = ""
    for i in range(10):
        password += password_char[random.randint(0, len(password_char) - 1)]
    
    return password
