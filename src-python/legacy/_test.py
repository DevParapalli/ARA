test = """ Here are two Python scripts to convert a binary number to a decimal number:\n1. Using the int() function with a base parameter of 2:\n```python\nbinary_num = '1101'\ndecimal_num = int(binary_num, 2)\nprint(decimal_num)\n```\n2. Using a for loop to iterate over each digit in the binary number and calculate the decimal equivalent:\n```python\ndef BinaryToDecimal(binary):\n    decimal = 0\n    for digit in binary:\n        decimal = decimal * 2 + int(digit)\n    return decimal\n\nbinary_num = '1101'\ndecimal_num = BinaryToDecimal(binary_num)\nprint(decimal_num)\n```\nBoth scripts assume the binary number is assigned to a string variable called `binary_num` and the decimal number is stored in a variable called `decimal_num`. The first script uses the `int()` function with a base parameter of 2 to convert the binary number to a decimal number. The second script uses a `for` loop to iterate over each digit in the binary number and calculate the decimal equivalent.\n\nThese scripts are straightforward and effective, converting a binary number to its decimal equivalent using the specified
"""

test.strip()


def _sanitize_output(text: str):
    import mistletoe
    from mistletoe.block_token import CodeFence

    # return re.split(r'```(python|c|cpp|js|javascript|rust)\n', text)
    doc = mistletoe.Document(text)
    for token in doc.children:
        if isinstance(token, CodeFence):
            yield {"language": token.language, "code": token.content}
    # return mistletoe.HtmlRenderer().render(doc)


def get_code_from_text(text: str):
    return list(_sanitize_output(text))


print(get_code_from_text(test))
