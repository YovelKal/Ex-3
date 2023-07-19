def make_test_logs(container_sum, pytest_code):
    str_builder = ""
    if container_sum > 0:
        str_builder += "Container up and running\n"
    else:
        str_builder += "Container failed to run\n"
        return str_builder
    if pytest_code == 0:
        str_builder += "tests succeeded\n"
    else:
        str_builder += "tests failed\n"

    return str_builder


if __name__ == '__main__':
    import sys
    container_sum = int(sys.argv[1])
    pytest_code = -1
    if len(sys.argv) > 2:
        pytest_code = int(sys.argv[2])
    print(make_test_logs(container_sum, pytest_code))

