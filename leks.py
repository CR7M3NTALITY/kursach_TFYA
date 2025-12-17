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
            else:
                if let(current_char):
                    CS = 'ER'
                else:
                    z = put_TN(buffer)
                    tokens.append((3, z))
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

    return tokens, TI, TN


# --- КОНЕЦ ЛЕКСИЧЕСКОГО АНАЛИЗАТОРА ---

# ==================== Синтаксический анализатор с Семантическими Проверками ====================

# --- Определение нового типа ошибки ---
class SemanticError(Exception):
    pass


# --- Глобальные переменные для синтаксического и семантического анализатора ---
tokens = []
pos = 0
TI_lexer = []
TN_lexer = []
TI_semantic = {}


def add_identifier(name, type_):
    if name in TI_semantic:
        raise SemanticError(f"Семантическая ошибка: переменная '{name}' уже объявлена.")
    TI_semantic[name] = {'type': type_, 'declared': True}


def check_identifier_declared(name):
    if name not in TI_semantic:
        raise SemanticError(f"Семантическая ошибка: переменная '{name}' не объявлена.")


def get_identifier_type(name):
    check_identifier_declared(name)
    return TI_semantic[name]['type']


def check_type_compatibility(op, type1, type2):
    if op in ['+', '-']:
        if type1 == 'integer' and type2 == 'integer':
            return 'integer'
        elif type1 in ['integer', 'real'] and type2 in ['integer', 'real']:
            return 'real'
        else:
            raise SemanticError(f"Семантическая ошибка: несовместимые типы для операции '{op}': {type1}, {type2}")
    elif op == '||':
        if type1 == 'boolean' and type2 == 'boolean':
            return 'boolean'
        else:
            raise SemanticError(f"Семантическая ошибка: операция '{op}' требует операнды типа 'boolean'")
    elif op == '&&':
        if type1 == 'boolean' and type2 == 'boolean':
            return 'boolean'
        else:
            raise SemanticError(f"Семантическая ошибка: операция '{op}' требует операнды типа 'boolean'")
    elif op in ['*', '/']:
        if type1 == 'integer' and type2 == 'integer':
            return 'integer'
        elif type1 in ['integer', 'real'] and type2 in ['integer', 'real']:
            return 'real'
        else:
            raise SemanticError(f"Семантическая ошибка: несовместимые типы для операции '{op}': {type1}, {type2}")
    elif op in ['!=', '==']:
        if type1 in ['integer', 'real'] and type2 in ['integer', 'real']:
            return 'boolean'
        elif type1 == 'boolean' and type2 == 'boolean':
            return 'boolean'
        else:
            raise SemanticError(f"Семантическая ошибка: операция '{op}' не поддерживается для типов: {type1}, {type2}")
    elif op in ['<', '<=', '>', '>=']:
        if type1 in ['integer', 'real'] and type2 in ['integer', 'real']:
            return 'boolean'
        else:
            raise SemanticError(f"Семантическая ошибка: операция '{op}' требует операнды типа 'integer' или 'real'")
    return None


def check_type_unary(op, type1):
    if op == '!':
        if type1 == 'boolean':
            return 'boolean'
        else:
            raise SemanticError(f"Семантическая ошибка: унарная операция '{op}' требует операнд типа 'boolean'")
    return None


def current_token():
    global pos
    if pos >= len(tokens):
        return None
    return tokens[pos]


def consume_token():
    global pos
    pos += 1


def match_table(table_num, index):
    tok = current_token()
    if tok and tok[0] == table_num and tok[1] == index:
        consume_token()
        return True
    return False


def match_any_in_table(table_num):
    tok = current_token()
    if tok and tok[0] == table_num:
        consume_token()
        return True
    return False


def parse_program():
    if not match_table(2, 1):  # {
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась '{{', найдена {current_token()}")
    parse_body()
    if not match_table(2, 2):  # }
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась '}}', найдена {current_token()}")


def parse_body():
    tok = current_token()
    if not tok:
        return
    if tok[0] == 1 and tok[1] == 1:  # dim
        parse_declaration()
        if not match_table(2, 20):  # ;
            raise SyntaxError(f"Синтаксическая ошибка: ожидалась ';', найдена {current_token()}")
        parse_body()
    elif tok[0] == 4 or (tok[0] == 1 and tok[1] in [5, 7, 11, 12, 14, 15]):
        parse_statement()
        if not match_table(2, 20):  # ;
            raise SyntaxError(f"Синтаксическая ошибка: ожидалась ';', найдена {current_token()}")
        parse_body()
    else:
        return


def parse_declaration():
    if not match_table(1, 1):  # dim
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'dim', найдена {current_token()}")

    def get_name_from_ti_idx(idx):
        if 1 <= idx <= len(TI_lexer):
            return TI_lexer[idx - 1]
        else:
            raise SemanticError(f"Семантическая ошибка: индекс идентификатора {idx} вне диапазона TI.")

    id_names = []
    # Сначала собираем все идентификаторы
    while True:
        current_pos_at_id = pos
        if not match_any_in_table(4):  # идентификатор
            raise SyntaxError(f"Синтаксическая ошибка: ожидался идентификатор в объявлении, найдена {current_token()}")
        token_at_id = tokens[current_pos_at_id]  # (4, Z)
        name = get_name_from_ti_idx(token_at_id[1])
        if name in id_names:
            raise SemanticError(f"Семантическая ошибка: дублирующийся идентификатор '{name}' в объявлении.")
        id_names.append(name)

        # Проверяем, идёт ли запятая
        if not match_table(2, 19):  # ,
            # Запятой нет, выходим из цикла
            break
        # Если запятая была, цикл продолжается, ожидаем следующий идентификатор

    # Теперь, после списка идентификаторов, ожидаем тип
    parse_type_internal()
    type_of_decl = last_parsed_type
    if type_of_decl is None:
        raise SyntaxError(f"Синтаксическая ошибка: не удалось определить тип в объявлении.")

    # Добавляем все идентификаторы в семантическую таблицу с этим типом
    for name in id_names:
        add_identifier(name, type_of_decl)


def parse_type_internal():
    global last_parsed_type
    if match_table(1, 2):  # integer
        last_parsed_type = 'integer'
        return
    elif match_table(1, 3):  # real
        last_parsed_type = 'real'
        return
    elif match_table(1, 4):  # boolean
        last_parsed_type = 'boolean'
        return
    else:
        last_parsed_type = None
        raise SyntaxError(f"Синтаксическая ошибка: ожидался тип (integer, real, boolean), найдена {current_token()}")


last_parsed_type = None


def parse_id_list():
    global TI_lexer
    current_pos_at_first_id = pos
    if not match_any_in_table(4):  # идентификатор
        raise SyntaxError(f"Синтаксическая ошибка: ожидался идентификатор в списке, найдена {current_token()}")
    token_at_first_id = tokens[current_pos_at_first_id]  # (4, Z)
    name = TI_lexer[token_at_first_id[1] - 1]
    check_identifier_declared(name)

    while match_table(2, 19):  # ,
        current_pos_for_next_id = pos
        if not match_any_in_table(4):  # идентификатор после запятой
            raise SyntaxError(f"Синтаксическая ошибка: ожидался идентификатор после ',', найдена {current_token()}")
        token_for_next_id = tokens[current_pos_for_next_id]  # (4, Z_next)
        next_name = TI_lexer[token_for_next_id[1] - 1]
        check_identifier_declared(next_name)


def parse_statement():
    tok = current_token()
    if not tok:
        raise SyntaxError("Синтаксическая ошибка: неожиданный конец входной цепочки в операторе")
    if tok[0] == 4:  # идентификатор -> присваивание
        parse_assignment()
    elif tok[0] == 1:
        if tok[1] == 5:  # if
            parse_if_statement()
        elif tok[1] == 7:  # for
            parse_for_statement()
        elif tok[1] == 11:  # while
            parse_while_statement()
        elif tok[1] == 12:  # begin
            parse_compound_statement()
        elif tok[1] == 14:  # readln
            parse_input_statement()
        elif tok[1] == 15:  # writeln
            parse_output_statement()
        else:
            raise SyntaxError(f"Синтаксическая ошибка: неожиданное ключевое слово в операторе: {tok}")
    else:
        raise SyntaxError(f"Синтаксическая ошибка: неожиданная лексема в операторе: {tok}")


def parse_assignment():
    global TI_lexer
    current_pos_at_ident = pos
    if not match_any_in_table(4):  # идентификатор
        raise SyntaxError(f"Синтаксическая ошибка: ожидался идентификатор в присваивании, найдена {current_token()}")
    token_at_ident = tokens[current_pos_at_ident]  # (4, Z)
    var_name = TI_lexer[token_at_ident[1] - 1]
    check_identifier_declared(var_name)
    var_type = get_identifier_type(var_name)

    if not match_table(2, 5):  # :=
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось ':=', найдена {current_token()}")

    expr_type = parse_expression()

    if var_type == 'integer' and expr_type not in ['integer']:
        raise SemanticError(f"Семантическая ошибка: несовместимый тип в присваивании. {var_type} = {expr_type}")
    elif var_type == 'real' and expr_type not in ['integer', 'real']:
        raise SemanticError(f"Семантическая ошибка: несовместимый тип в присваивании. {var_type} = {expr_type}")
    elif var_type == 'boolean' and expr_type != 'boolean':
        raise SemanticError(f"Семантическая ошибка: несовместимый тип в присваивании. {var_type} = {expr_type}")


def parse_if_statement():
    if not match_table(1, 5):  # if
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'if', найдена {current_token()}")
    if not match_table(2, 3):  # (
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась '(', найдена {current_token()}")
    expr_type = parse_expression()
    if expr_type != 'boolean':
        raise SemanticError(f"Семантическая ошибка: условие в 'if' должно быть типа 'boolean', получено {expr_type}")
    if not match_table(2, 4):  # )
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась ')', найдена {current_token()}")
    parse_statement()
    if match_table(1, 6):  # else
        parse_statement()


def parse_for_statement():
    global TI_lexer
    if not match_table(1, 7):  # for
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'for', найдена {current_token()}")

    current_pos_at_counter = pos
    if not match_any_in_table(4):  # идентификатор (счётчик)
        raise SyntaxError(f"Синтаксическая ошибка: ожидался идентификатор (счётчик) в for, найдена {current_token()}")
    token_at_counter = tokens[current_pos_at_counter]  # (4, Z)
    counter_name = TI_lexer[token_at_counter[1] - 1]
    check_identifier_declared(counter_name)
    counter_type = get_identifier_type(counter_name)
    if counter_type != 'integer':
        raise SemanticError(f"Семантическая ошибка: счётчик в 'for' должен быть типа 'integer', получен {counter_type}")

    if not match_table(2, 5):  # :=
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось ':=' после счётчика в for, найдена {current_token()}")
    start_expr_type = parse_expression()
    if start_expr_type != 'integer':
        raise SemanticError(
            f"Семантическая ошибка: начальное значение в 'for' должно быть типа 'integer', получено {start_expr_type}")

    if not match_table(1, 8):  # to
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'to' в for, найдена {current_token()}")
    end_expr_type = parse_expression()
    if end_expr_type != 'integer':
        raise SemanticError(
            f"Семантическая ошибка: конечное значение в 'for' должно быть типа 'integer', получено {end_expr_type}")

    if match_table(1, 9):  # step
        step_expr_type = parse_expression()
        if step_expr_type != 'integer':
            raise SemanticError(
                f"Семантическая ошибка: шаг в 'for' должен быть типа 'integer', получено {step_expr_type}")

    parse_statement()

    if not match_table(1, 10):  # next
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'next' в for, найдена {current_token()}")


def parse_while_statement():
    if not match_table(1, 11):  # while
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'while', найдена {current_token()}")
    if not match_table(2, 3):  # (
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась '(', найдена {current_token()}")
    expr_type = parse_expression()
    if expr_type != 'boolean':
        raise SemanticError(f"Семантическая ошибка: условие в 'while' должно быть типа 'boolean', получено {expr_type}")
    if not match_table(2, 4):  # )
        raise SyntaxError(f"Синтаксическая ошибка: ожидалась ')', найдена {current_token()}")
    parse_statement()


def parse_compound_statement():
    if not match_table(1, 12):  # begin
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'begin', найдена {current_token()}")
    parse_statement()
    while match_table(2, 20):  # ;
        parse_statement()
    if not match_table(1, 13):  # end
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'end', найдена {current_token()}")


def parse_input_statement():
    if not match_table(1, 14):  # readln
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'readln', найдена {current_token()}")
    parse_id_list()


def parse_output_statement():
    if not match_table(1, 15):  # writeln
        raise SyntaxError(f"Синтаксическая ошибка: ожидалось 'writeln', найдена {current_token()}")
    parse_expr_list()


def parse_expr_list():
    parse_expression()
    while match_table(2, 19):  # ,
        parse_expression()


def parse_expression():
    return parse_relation()


def parse_relation():
    left_type = parse_sum()
    tok = current_token()
    if tok and tok[0] == 2 and tok[1] in [6, 7, 8, 9, 10, 11]:  # !=, ==, <, <=, >, >=
        op_map = {6: '!=', 7: '==', 8: '<', 9: '<=', 10: '>', 11: '>='}
        op = op_map[tok[1]]
        consume_token()
        right_type = parse_sum()
        result_type = check_type_compatibility(op, left_type, right_type)
        return result_type
    return left_type


def parse_sum():
    left_type = parse_product()
    while True:
        tok = current_token()
        if tok and tok[0] == 2 and tok[1] in [12, 13, 14]:  # +, -, ||
            op_map = {12: '+', 13: '-', 14: '||'}
            op = op_map[tok[1]]
            consume_token()
            right_type = parse_product()
            left_type = check_type_compatibility(op, left_type, right_type)
        else:
            break
    return left_type


def parse_product():
    left_type = parse_factor()
    while True:
        tok = current_token()
        if tok and tok[0] == 2 and tok[1] in [15, 16, 17]:  # *, /, &&
            op_map = {15: '*', 16: '/', 17: '&&'}
            op = op_map[tok[1]]
            consume_token()
            right_type = parse_factor()
            left_type = check_type_compatibility(op, left_type, right_type)
        else:
            break
    return left_type


def parse_factor():
    tok = current_token()
    if not tok:
        raise SyntaxError("Синтаксическая ошибка: неожиданный конец входной цепочки в факторе")
    if tok[0] == 4:  # идентификатор
        name = TI_lexer[tok[1] - 1]
        check_identifier_declared(name)
        consume_token()
        return get_identifier_type(name)
    elif tok[0] == 3:  # число
        num_str = TN_lexer[tok[1] - 1]
        consume_token()
        if '.' in num_str or 'E' in num_str.upper():
            return 'real'
        else:
            return 'integer'
    elif tok[0] == 1 and tok[1] in [16, 17]:  # true, false
        consume_token()
        return 'boolean'
    elif match_table(2, 18):  # !
        operand_type = parse_factor()
        result_type = check_type_unary('!', operand_type)
        return result_type
    elif match_table(2, 3):  # (
        result_type = parse_expression()
        if not match_table(2, 4):  # )
            raise SyntaxError(f"Синтаксическая ошибка: ожидалась ')', найдена {current_token()}")
        return result_type
    else:
        raise SyntaxError(f"Синтаксическая ошибка: неожиданная лексема в факторе: {tok}")


def syntax_analyzer(input_tokens, ti_list, tn_list):
    global tokens, pos, TI_semantic, TI_lexer, TN_lexer
    tokens = input_tokens
    pos = 0
    TI_lexer = ti_list
    TN_lexer = tn_list
    TI_semantic.clear()
    try:
        parse_program()
        if pos < len(tokens):
            raise SyntaxError(f"Синтаксическая ошибка: осталась необработанная лексема: {tokens[pos]} на позиции {pos}")
        print("Программа синтаксически и семантически корректна.")
        return True
    except SyntaxError as e:
        print(f"Ошибка: {e}")
        return False
    except SemanticError as e:
        print(f"Ошибка: {e}")
        return False


if __name__ == "__main__":
    sample_code = """ {
  dim x, y integer;
  dim r real;
  dim flag boolean;
  x := 10;
  y := x + 5;
  r := x / y;
  flag := (r > 3.0);
  writeln x, y, r, flag; 
  } """

    print("Код программы:")
    print(sample_code)
    print("\nЦепочка лексем (номер_таблицы, номер_в_таблице):")
    try:
        tokens_from_lexer, TI_lexed, TN_lexed = lexer(sample_code)
        for t in tokens_from_lexer:
            print(t)

        print("\n--- Запуск синтаксического и семантического анализа ---")
        syntax_analyzer(tokens_from_lexer, TI_lexed, TN_lexed)

    except SyntaxError as e:
        print(f"Ошибка лексического анализа: {e}")
    except SemanticError as e:
        print(
            f"Ошибка лексического анализа (ожидается SemErr, но бросается SynErr): {e}")  # Это не должно сработать на данном коде
