#!/usr/bin/env python3

def main():
    valid_password_count = 0

    for password in range(147981, 691423+1):
        if is_password_valid(str(password)):
            valid_password_count += 1

    print('Valid passwords:', valid_password_count)

def is_password_valid(password: str) -> bool:
    if not contains_double_digits(password):
        return False

    if not contains_increasing_digits(password):
        return False

    return True

def contains_double_digits(password: str) -> bool:
    for a, b in zip(password, password[1:]):
        if a == b:
            return True
    return False

def contains_increasing_digits(password: str) -> bool:
    for a, b in zip(password, password[1:]):
        if b < a:
            return False
    return True

if __name__ == '__main__':
    main()
