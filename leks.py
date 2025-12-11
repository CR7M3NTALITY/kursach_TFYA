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
                tokens.append((2, 1))
                gc()
            elif current_char == '}':
                tokens.append((2, 2))
                gc()
            elif current_char == '(':
                tokens.append((2, 3))
                gc()
            elif current_char == ')':
                tokens.append((2, 4))
                gc()
            elif current_char == ':':
                gc()
                if current_char == '=':
                    tokens.append((2, 5))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '!':
                gc()
                if current_char == '=':
                    tokens.append((2, 6))
                    gc()
                else:
                    tokens.append((2, 18))
                    gc()
            elif current_char == '=':
                gc()
                if current_char == '=':
                    tokens.append((2, 7))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '<':
                gc()
                if current_char == '=':
                    tokens.append((2, 9))
                    gc()
                else:
                    tokens.append((2, 8))
            elif current_char == '>':
                gc()
                if current_char == '=':
                    tokens.append((2, 11))
                    gc()
                else:
                    tokens.append((2, 10))
            elif current_char == '+':
                tokens.append((2, 12))
                gc()
            elif current_char == '-':
                tokens.append((2, 13))
                gc()
            elif current_char == '*':
                tokens.append((2, 15))
                gc()
            elif current_char == '/':
                gc()
                if current_char == '*':
                    gc()
                    CS = 'C1'
                else:
                    tokens.append((2, 16))
            elif current_char == '&':
                gc()
                if current_char == '&':
                    tokens.append((2, 17))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == '|':
                gc()
                if current_char == '|':
                    tokens.append((2, 14))
                    gc()
                else:
                    CS = 'ER'
            elif current_char == ',':
                tokens.append((2, 19))
                gc()
            elif current_char == ';':
                tokens.append((2, 20))
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
                    tokens.append((3, z))
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
                    tokens.append((3, z))
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
                    tokens.append((3, z))
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
                tokens.append((3, z))
                nill()
                gc()
                CS = 'H'
            else:  # Просто целое десятичное *или* ошибка
                if let(current_char):
                    CS = 'ER'
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
                tokens.append((3, z))
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
            tokens.append((3, z))
            nill()
            CS = 'H'

        elif CS == 'I':
            while let(current_char) or digit(current_char):
                add()
                gc()
            z = TW.get(buffer, 0)
            if z != 0:
                tokens.append((1, z))
            else:
                z = put_TI(buffer)
                tokens.append((4, z))
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

tokens = []  # Цепочка лексем, полученная от лексического анализатора
pos = 0      # Текущая позиция в цепочке лексем

def current_token():
    """Возвращает текущую лексему без её извлечения."""
    global pos
    if pos >= len(tokens):
        return None
    return tokens[pos]

def consume_token():
    """Считывает (пропускает) текущую лексему."""
    global pos
    pos += 1

def match_table(table_num, index):
    """
    Проверяет, совпадает ли текущая лексема с (table_num, index).
    """
    tok = current_token()
    if tok and tok[0] == table_num and tok[1] == index:
        consume_token()
        return True
    return False

def match_any_in_table(table_num):
    """
    Проверяет, совпадает ли текущая лексема с любой из таблицы table_num.
    """
    tok = current_token()
    if tok and tok[0] == table_num:
        consume_token()
        return True
    return False

def parse_program():
    """
    <program> → { <body> }
    """
    if not match_table(2, 1):  # {
        raise SyntaxError(f"Ошибка: ожидалась '{{', найдена {current_token()}")
    parse_body()
    if not match_table(2, 2):  # }
        raise SyntaxError(f"Ошибка: ожидалась '}}', найдена {current_token()}")

def parse_body():
    """
    <body> → <declaration_or_statement> ; <body>
          | ε (пустая цепочка - программа может быть {})
    """
    tok = current_token()
    if not tok:
        return  # ε (пустая цепочка)
    # Пробуем распознать <declaration_or_statement>
    # Это может быть dim (1,1), или идентификатор (4, x), или служебное слово (1, x)
    # Надо смотреть вперёд.
    if tok[0] == 1 and tok[1] == 1:  # dim
        parse_declaration()
        if not match_table(2, 20):  # ;
            raise SyntaxError(f"Ошибка: ожидалась ';', найдена {current_token()}")
        parse_body() # Рекурсивный вызов для оставшейся части
    elif tok[0] == 4 or (tok[0] == 1 and tok[1] in [5, 7, 11, 12, 14, 15]):  # идентификатор или if, for, while, begin, readln, writeln
        parse_statement()
        if not match_table(2, 20):  # ;
            raise SyntaxError(f"Ошибка: ожидалась ';', найдена {current_token()}")
        parse_body() # Рекурсивный вызов для оставшейся части
    else:
        return

def parse_declaration():
    """
    <declaration> → dim <id_list> <type>
    """
    if not match_table(1, 1):
        raise SyntaxError(f"Ошибка: ожидалось 'dim', найдена {current_token()}")
    parse_id_list()
    parse_type()

def parse_id_list():
    """
    <id_list> → <identifier> , <id_list>
             | <identifier>
    """
    if not match_any_in_table(4):  # идентификатор
        raise SyntaxError(f"Ошибка: ожидался идентификатор в объявлении, найдена {current_token()}")
    # Проверяем, есть ли запятая
    while match_table(2, 19):  # ,
        if not match_any_in_table(4):  # идентификатор после запятой
            raise SyntaxError(f"Ошибка: ожидался идентификатор после ',', найдена {current_token()}")

def parse_type():
    """
    <type> → integer
           | real
           | boolean
    """
    if match_table(1, 2):  # integer
        return
    elif match_table(1, 3):  # real
        return
    elif match_table(1, 4):  # boolean
        return
    else:
        raise SyntaxError(f"Ошибка: ожидался тип (integer, real, boolean), найдена {current_token()}")

def parse_statement():
    """
    <statement> → <assignment>
                | <if_statement>
                | <for_statement>
                | <while_statement>
                | <compound_statement>
                | <input_statement>
                | <output_statement>
    """
    tok = current_token()
    if not tok:
        raise SyntaxError("Ошибка: неожиданный конец входной цепочки в операторе")
    # Смотрим, с чего начинается оператор
    if tok[0] == 4:  # идентификатор -> присваивание
        parse_assignment()
    elif tok[0] == 1:
        if tok[1] == 5:  # if
            parse_if_statement()
        elif tok[1] == 7:  # for
            parse_for_statement()
        elif tok[1] == 11: # while
            parse_while_statement()
        elif tok[1] == 12: # begin
            parse_compound_statement()
        elif tok[1] == 14: # readln
            parse_input_statement()
        elif tok[1] == 15: # writeln
            parse_output_statement()
        else:
            raise SyntaxError(f"Ошибка: неожиданное ключевое слово в операторе: {tok}")
    else:
        raise SyntaxError(f"Ошибка: неожиданная лексема в операторе: {tok}")

def parse_assignment():
    """
    <assignment> → <identifier> := <expression>
    """
    if not match_any_in_table(4):  # идентификатор
        raise SyntaxError(f"Ошибка: ожидался идентификатор в присваивании, найдена {current_token()}")
    if not match_table(2, 5):  # :=
        raise SyntaxError(f"Ошибка: ожидалось ':=', найдена {current_token()}")
    parse_expression()

def parse_if_statement():
    """
    <if_statement> → if ( <expression> ) <statement> [else <statement>]
    """
    if not match_table(1, 5):  # if
        raise SyntaxError(f"Ошибка: ожидалось 'if', найдена {current_token()}")
    if not match_table(2, 3):  # (
        raise SyntaxError(f"Ошибка: ожидалась '(', найдена {current_token()}")
    parse_expression()
    if not match_table(2, 4):  # )
        raise SyntaxError(f"Ошибка: ожидалась ')', найдена {current_token()}")
    parse_statement()
    if match_table(1, 6):  # else
        parse_statement()

def parse_for_statement():
    """
    <for_statement> → for <assignment> to <expression> [step <expression>] <statement> next
    """
    if not match_table(1, 7):  # for
        raise SyntaxError(f"Ошибка: ожидалось 'for', найдена {current_token()}")
    parse_assignment() # Счётчик
    if not match_table(1, 8):  # to
        raise SyntaxError(f"Ошибка: ожидалось 'to', найдена {current_token()}")
    parse_expression() # Граница
    if match_table(1, 9):  # step
        parse_expression() # Шаг
    parse_statement() # Тело
    if not match_table(1, 10):  # next
        raise SyntaxError(f"Ошибка: ожидалось 'next', найдена {current_token()}")

def parse_while_statement():
    """
    <while_statement> → while ( <expression> ) <statement>
    """
    if not match_table(1, 11): # while
        raise SyntaxError(f"Ошибка: ожидалось 'while', найдена {current_token()}")
    if not match_table(2, 3):  # (
        raise SyntaxError(f"Ошибка: ожидалась '(', найдена {current_token()}")
    parse_expression()
    if not match_table(2, 4):  # )
        raise SyntaxError(f"Ошибка: ожидалась ')', найдена {current_token()}")
    parse_statement()

def parse_compound_statement():
    """
    <compound_statement> → begin <statement> ; <statement_list> end
    """
    if not match_table(1, 12): # begin
        raise SyntaxError(f"Ошибка: ожидалось 'begin', найдена {current_token()}")
    parse_statement()
    while match_table(2, 20):  # ;
        parse_statement()
    if not match_table(1, 13): # end
        raise SyntaxError(f"Ошибка: ожидалось 'end', найдена {current_token()}")

def parse_input_statement():
    """
    <input_statement> → readln <id_list>
    """
    if not match_table(1, 14): # readln
        raise SyntaxError(f"Ошибка: ожидалось 'readln', найдена {current_token()}")
    parse_id_list()

def parse_output_statement():
    """
    <output_statement> → writeln <expr_list>
    """
    if not match_table(1, 15): # writeln
        raise SyntaxError(f"Ошибка: ожидалось 'writeln', найдена {current_token()}")
    parse_expr_list()

def parse_expr_list():
    """
    <expr_list> → <expression> , <expr_list>
                 | <expression>
    """
    parse_expression()
    while match_table(2, 19): # ,
        parse_expression()

def parse_expression():
    """
    <expression> → <relation>
    """
    parse_relation()

def parse_relation():
    """
    <relation> → <sum> <relation_tail>
    <relation_tail> → != <sum> <relation_tail>
                    | == <sum> <relation_tail>
                    | < <sum> <relation_tail>
                    | <= <sum> <relation_tail>
                    | > <sum> <relation_tail>
                    | >= <sum> <relation_tail>
                    | ε
    """
    parse_sum()
    # Проверяем, идёт ли операция отношения
    tok = current_token()
    if tok and tok[0] == 2 and tok[1] in [6, 7, 8, 9, 10, 11]: # !=, ==, <, <=, >, >=
        consume_token() # Пропускаем операцию
        parse_sum() # Правый операнд
        # Продолжаем проверять, может быть цепочка: a < b <= c
        parse_relation_tail()

def parse_relation_tail():
    """
    Вспомогательная функция для цепочек операций отношения.
    """
    tok = current_token()
    if tok and tok[0] == 2 and tok[1] in [6, 7, 8, 9, 10, 11]: # !=, ==, <, <=, >, >=
        consume_token() # Пропускаем операцию
        parse_sum() # Правый операнд
        parse_relation_tail() # Рекурсивно проверяем дальше

def parse_sum():
    """
    <sum> → <product> <sum_tail>
    <sum_tail> → + <product> <sum_tail>
               | - <product> <sum_tail>
               | || <product> <sum_tail>
               | ε
    """
    parse_product()
    parse_sum_tail()

def parse_sum_tail():
    """
    Вспомогательная функция для цепочек операций сложения.
    """
    tok = current_token()
    if tok and tok[0] == 2 and tok[1] in [12, 13, 14]: # +, -, ||
        consume_token() # Пропускаем операцию
        parse_product() # Правый операнд
        parse_sum_tail() # Рекурсивно проверяем дальше

def parse_product():
    """
    <product> → <factor> <product_tail>
    <product_tail> → * <factor> <product_tail>
                   | / <factor> <product_tail>
                   | && <factor> <product_tail>
                   | ε
    """
    parse_factor()
    parse_product_tail()

def parse_product_tail():
    """
    Вспомогательная функция для цепочек операций умножения.
    """
    tok = current_token()
    if tok and tok[0] == 2 and tok[1] in [15, 16, 17]: # *, /, &&
        consume_token() # Пропускаем операцию
        parse_factor() # Правый операнд
        parse_product_tail() # Рекурсивно проверяем дальше

def parse_factor():
    """
    <factor> → <identifier>
             | <number>
             | <logical_constant>
             | ! <factor>
             | ( <expression> )
    """
    tok = current_token()
    if not tok:
        raise SyntaxError("Ошибка: неожиданный конец входной цепочки в факторе")
    if tok[0] == 4:  # идентификатор
        consume_token()
    elif tok[0] == 3:  # число
        consume_token()
    elif tok[0] == 1 and tok[1] in [16, 17]: # true, false
        consume_token()
    elif match_table(2, 18):  # !
        parse_factor() # Правый операнд унарной операции
    elif match_table(2, 3):  # (
        parse_expression()
        if not match_table(2, 4):  # )
            raise SyntaxError(f"Ошибка: ожидалась ')', найдена {current_token()}")
    else:
        raise SyntaxError(f"Ошибка: неожиданная лексема в факторе: {tok}")

def syntax_analyzer(input_tokens):
    """
    Основная функция синтаксического анализатора.
    Принимает цепочку лексем и проверяет синтаксис.
    """
    global tokens, pos
    tokens = input_tokens
    pos = 0
    try:
        parse_program()
        if pos < len(tokens):
            # Если после разбора остались необработанные лексемы
            raise SyntaxError(f"Ошибка: осталась необработанная лексема: {tokens[pos]} на позиции {pos}")
        print("Программа синтаксически корректна.")
        return True
    except SyntaxError as e:
        print(f"Ошибка синтаксического анализа: {e}")
        return False

if __name__ == "__main__":
    # Пример кода для тестирования
    sample_code = """ {
  dim x, y integer;
  dim r real;
  dim flag boolean;
  x := 10k;
  y := x + 5;
  r := x / y;
  z := 0100101B;
  flag := (r > 3.0);
  writeln x, y, r, flag; 
  } """

    print("Код программы:")
    print(sample_code)


    try:
        tokens_from_lexer = lexer(sample_code)
        print("\nЦепочка лексем (номер_таблицы, номер_в_таблице):")
        for t in tokens_from_lexer:
            print(t)

        print("\nЗапуск синтаксического анализа")
        syntax_analyzer(tokens_from_lexer)

    except SyntaxError as e:
        print(f"Ошибка: {e}")
