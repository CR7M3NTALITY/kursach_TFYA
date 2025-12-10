KEYWORDS = [
    "dim",
    "integer",
    "real",
    "boolean",
    "if",
    "else",
    "for",
    "to",
    "step",
    "next",
    "while",
    "begin",
    "end",
    "readln",
    "writeln",
    "true",
    "false"
]

SEPARATORS = [
    "{",
    "}",
    "(",
    ")",
    ":=",
    "!=",
    "==",
    "<",
    "<=",
    ">",
    ">=",
    "+",
    "-",
    "||",
    "*",
    "/",
    "&&",
    "!",
    ",",
    ";",
    "/*",
    "*/"
]

TW = {word: i + 1 for i, word in enumerate(KEYWORDS)}
TL = {sep: i + 1 for i, sep in enumerate(SEPARATORS)}

def let(ch):
    return ch.isalpha() and ch.isascii()

def digit(ch):
    return ch.isdigit()

def is_hex_digit(ch):
    return ch.isdigit() or ch.upper() in 'ABCDEF'

def lexer(text):
    text += "\0"
    pos = 0
    current_char = text[pos]
    buffer = ""
    tokens = []
    TI = []  # идентификаторы: список строк
    TN = []  # числа: список строк

    def gc():
        nonlocal pos, current_char
        pos += 1
        if pos >= len(text):
            current_char = "\0"
        else:
            current_char = text[pos]

    def add():
        nonlocal buffer
        buffer += current_char

    def nill():
        nonlocal buffer
        buffer = ""

    def put_TI(value):
        if value not in TI:
            TI.append(value)
        return TI.index(value) + 1

    def put_TN(value):
        if value not in TN:
            TN.append(value)
        return TN.index(value) + 1

    CS = 'H'  # начальное состояние

    while CS != 'ER' and current_char != "\0":
        if CS == 'H':
            if current_char.isspace():
                gc()
                continue
            if let(current_char):
                nill()
                add()
                gc()
                CS = 'I'
            elif digit(current_char):
                nill()
                add()
                gc()
                CS = 'N10'
            elif current_char == '{':
                tokens.append((2, 1, '{', CS))
                gc()
            elif current_char == '}':
                tokens.append((2, 2, '}', CS))
                gc()
            elif current_char == '(':
                tokens.append((2, 3, '(', CS))
                gc()
            elif current_char == ')':
                tokens.append((2, 4, ')', CS))
                gc()
            elif current_char == ':':
                gc()
                if current_char == '=':
                    tokens.append((2, 5, ":=", CS))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '!':
                gc()
                if current_char == '=':
                    tokens.append((2, 6, "!=", CS))
                    gc()
                else:
                    tokens.append((2, 18, "!", CS))
                    gc()
            elif current_char == '=':
                gc()
                if current_char == '=':
                    tokens.append((2, 7, "==", CS))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '<':
                gc()
                if current_char == '=':
                    tokens.append((2, 9, "<=", CS))
                    gc()
                else:
                    tokens.append((2, 8, "<", CS))
            elif current_char == '>':
                gc()
                if current_char == '=':
                    tokens.append((2, 11, ">=", CS))
                    gc()
                else:
                    tokens.append((2, 10, ">", CS))
            elif current_char == '+':
                tokens.append((2, 12, "+", CS))
                gc()
            elif current_char == '-':
                tokens.append((2, 13, "-", CS))
                gc()
            elif current_char == '*':
                tokens.append((2, 15, "*", CS))
                gc()
            elif current_char == '/':
                gc()
                if current_char == '*':
                    gc()
                    CS = 'C1'
                else:
                    tokens.append((2, 16, "/", CS))
            elif current_char == '&':
                gc()
                if current_char == '&':
                    tokens.append((2, 17, "&&", CS))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '|':
                gc()
                if current_char == '|':
                    tokens.append((2, 14, "||", CS))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == ',':
                tokens.append((2, 19, ",", CS))
                gc()
            elif current_char == ';':
                tokens.append((2, 20, ";", CS))
                gc()
            else:
                CS = 'ER'

        elif CS == 'N10':
            while digit(current_char):
                add()
                gc()

            if current_char in 'Bb':
                if all(c in '01' for c in buffer):
                    CS = 'N2'
                    add()
                    gc()
                    z = put_TN(buffer)
                    tokens.append((3, z, buffer, CS))
                    nill()
                    CS = 'H'
                else:
                    CS = 'ER'

            elif current_char in 'Oo':
                if all(c in '01234567' for c in buffer):
                    CS = 'N8'
                    add()
                    gc()
                    z = put_TN(buffer)
                    tokens.append((3, z, buffer, CS))
                    nill()
                    CS = 'H'
                else:

                    CS = 'ER'

            elif current_char in 'Hh':
                if all(is_hex_digit(c) for c in buffer):
                    CS = 'N16'
                    add()
                    gc()
                    z = put_TN(buffer)
                    tokens.append((3, z, buffer, CS))
                    nill()
                    CS = 'H'
                else:

                    CS = 'ER'

            elif current_char == '.':
                add()
                gc()
                CS = 'P1'
            elif current_char in 'Ee':
                add()
                gc()
                CS = 'E11'
            elif current_char in 'Dd':
                add()
                gc()
                z = put_TN(buffer)
                tokens.append((3, z, buffer, CS))
                nill()
                gc()
                CS = 'H'
            else:
                z = put_TN(buffer)
                tokens.append((3, z, buffer, CS))
                nill()
                CS = 'H'

        elif CS == 'P1':
            if digit(current_char):
                CS = 'P2'
            else:
                CS = 'ER'

        elif CS == 'P2':
            while digit(current_char):
                add()
                gc()
            if current_char in 'Ee':
                add()
                gc()
                CS = 'E11'
            else:
                z = put_TN(buffer)
                tokens.append((3, z, buffer, CS))
                nill()
                CS = 'H'

        elif CS == 'E11':
            if current_char in '+-':
                add()
                gc()
            if digit(current_char):
                CS = 'E12'
            else:
                CS = 'ER'

        elif CS == 'E12':
            while digit(current_char):
                add()
                gc()
            z = put_TN(buffer)
            tokens.append((3, z, buffer, CS))
            nill()
            CS = 'H'

        elif CS == 'I':
            while let(current_char) or digit(current_char):
                add()
                gc()
            z = TW.get(buffer, 0)
            if z != 0:
                tokens.append((1, z, buffer, CS))
            else:
                z = put_TI(buffer)
                tokens.append((4, z, buffer, CS))
            nill()
            CS = 'H'

        elif CS == 'C1':
            while current_char != '*' and current_char != "\0":
                gc()
            if current_char == '*':
                gc()
                if current_char == '/':
                    gc()
                    CS = 'H'
                else:
                    CS = 'ER'
            else:
                CS = 'ER'

        else:
            CS = 'ER'

    if CS == 'ER':
        raise SyntaxError(f"Ошибка лексического анализа. Недопустимый символ или последовательность: '{current_char}'.")

    return tokens

if __name__ == "__main__":
    # Примеры чисел
    sample_code = """
    {
      dim a, b, integer;
      a := 10;
      b := 0101B;  /* двоичное */
      writeln 077O, 0A1H, 3.14, 0, 010;
    }
    """

    print("Код программы:")
    print(sample_code)
    print("\nЦепочка лексем (номер_таблицы, номер_в_таблице, лексема, состояние):")
    try:
        tokens = lexer(sample_code)
        for t in tokens:
            print(t)
    except SyntaxError as e:
        print(f"Ошибка: {e}")