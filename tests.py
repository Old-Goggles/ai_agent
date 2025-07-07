from functions.get_file_content import get_file_content


if __name__ == "__main__":
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    returned_content = get_file_content("calculator", "/bin/cat")
    error_result = returned_content.startswith("Error")
    if error_result == True:
        print(f"{returned_content} Error Test Passed")
    else:
        print(f"{returned_content} Error Test Failed")