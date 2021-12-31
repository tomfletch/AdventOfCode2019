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
    current_digit = ''
    current_digit_count = 0

    for next_digit in password:
        if next_digit != current_digit:
            if current_digit_count == 2:
                return True

            current_digit = next_digit
            current_digit_count = 1
        else:
            current_digit_count += 1

    return current_digit_count == 2

def contains_increasing_digits(password: str) -> bool:
    for a, b in zip(password, password[1:]):
        if b < a:
            return False
    return True

if __name__ == '__main__':
    main()
