import shrike
from shrike.compliant_logging.exceptions import prefix_stack_trace


@prefix_stack_trace(prefix="MyCustomPrefix")
def custom_prefix():
    print(1 / 0)


@prefix_stack_trace(scrub_message="Private data was divided by zero")
def custom_message():
    print(1 / 0)


@prefix_stack_trace(keep_message=True)
def keep_exception_message():
    print(1 / 0)


@prefix_stack_trace(keep_message=False, allow_list=["ZeroDivision"])
def keep_allowed_exceptions():
    print(1 / 0)


@prefix_stack_trace(add_timestamp=True)
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
