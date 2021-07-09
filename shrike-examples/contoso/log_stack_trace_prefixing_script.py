# To-Do: import relevant libraries


# To-Do: decorator with custom prefix
def custom_prefix():
    print(1 / 0)


# To-Do: decorator with custom message
def custom_message():
    print(1 / 0)


# To-Do: decorator with exception message displayed
def keep_exception_message():
    print(1 / 0)


# To-Do: decorator with allow-list for exceptions
def keep_allowed_exceptions():
    print(1 / 0)


# To-Do: decorator with timestamp displayed in logs
def add_timestamp():
    print(1 / 0)


def main():
    try:
        custom_prefix()
    except:
        pass
    try:
        custom_message()
    except:
        pass
    try:
        keep_exception_message()
    except:
        pass
    try:
        keep_allowed_exceptions()
    except:
        pass
    try:
        add_timestamp()
    except:
        pass


if __name__ == "__main__":
    main()
