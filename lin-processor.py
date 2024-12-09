import re

file_c = open('code.txt', encoding='utf-8')


code =  file_c.read()
print(f'---------{code}')
# Парсер и интерпретатор
class SimpleLanguage:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.keywords = {
            "если": self.if_statement,
            "иначе": self.else_statement,
            "повторить": self.loop,
            "функция": self.function_definition,
            "вернуть": self.return_statement,
            "вывод": self.output,
        }
        self.current_function = None

    def parse(self, code):
        lines = code.split("\n")
        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        line = line.strip()
        if not line:
            return

        # Проверка на ключевые слова
        for keyword, handler in self.keywords.items():
            if line.startswith(keyword):
                handler(line)
                return

        # Проверка на присваивание переменной
        if "=" in line:
            self.assign_variable(line)
            return

        # Проверка на вызов функции
        if "(" in line and ")" in line:
            self.call_function(line)
            return

    def assign_variable(self, line):
        var_name, value = line.split("=", 1)
        var_name = var_name.strip()
        value = value.strip()
        if value.isdigit():
            self.variables[var_name] = int(value)
        elif value.startswith('"') and value.endswith('"'):
            self.variables[var_name] = value[1:-1]
        elif value == "правда" or value == "ложь":
            self.variables[var_name] = value == "правда"
        elif "+" in value or "-" in value or "*" in value or "/" in value:
            self.variables[var_name] = self.evaluate_expression(value)
        elif "(" in value and ")" in value:
            self.variables[var_name] = self.call_function(value)
        else:
            self.variables[var_name] = self.variables[value]

    def evaluate_expression(self, expression):
        tokens = re.findall(r'\d+|\w+|[+\-*/]', expression)
        result = self.evaluate_token(tokens[0])
        for i in range(1, len(tokens), 2):
            operator = tokens[i]
            operand = self.evaluate_token(tokens[i+1])
            if operator == "+":
                result += operand
            elif operator == "-":
                result -= operand
            elif operator == "*":
                result *= operand
            elif operator == "/":
                result /= operand
        return result

    def evaluate_token(self, token):
        if token.isdigit():
            return int(token)
        elif token in self.variables:
            return self.variables[token]
        elif "(" in token and ")" in token:
            return self.call_function(token)
        return token

    def if_statement(self, line):
        condition, block = line.split("то", 1)
        condition = condition.replace("если", "").strip()
        block = block.strip()
        if self.evaluate_condition(condition):
            self.parse_block(block)

    def else_statement(self, line):
        block = line.replace("иначе", "").strip()
        self.parse_block(block)

    def loop(self, line):
        count, block = line.split("раз", 1)
        count = int(count.replace("повторить", "").strip())
        block = block.strip()
        for _ in range(count):
            self.parse_block(block)

    def function_definition(self, line):
        func_name, params_block = line.split("(", 1)
        func_name = func_name.replace("функция", "").strip()
        params, block = params_block.split(")", 1)
        params = [p.strip() for p in params.split(",")]
        block = block.strip()
        self.functions[func_name] = (params, block)

    def call_function(self, line):
        func_name, args_block = line.split("(", 1)
        func_name = func_name.strip()
        args, _ = args_block.split(")", 1)
        args = [self.evaluate_token(a.strip()) for a in args.split(",")]
        params, block = self.functions[func_name]
        old_vars = self.variables.copy()
        for param, arg in zip(params, args):
            self.variables[param] = arg
        self.parse_block(block)
        result = self.variables.get("return", None)
        self.variables = old_vars
        return result

    def return_statement(self, line):
        value = line.replace("вернуть", "").strip()
        if value in self.variables:
            self.variables["return"] = self.variables[value]
        else:
            self.variables["return"] = self.evaluate_token(value)

    def output(self, line):
        value = line.replace("вывод", "").strip()
        if value in self.variables:
            print(self.variables[value])
        else:
            print(value)

    def evaluate_condition(self, condition):
        if "==" in condition:
            left, right = condition.split("==", 1)
            return self.evaluate_token(left.strip()) == self.evaluate_token(right.strip())
        elif "<" in condition:
            left, right = condition.split("<", 1)
            return self.evaluate_token(left.strip()) < self.evaluate_token(right.strip())
        elif ">" in condition:
            left, right = condition.split(">", 1)
            return self.evaluate_token(left.strip()) > self.evaluate_token(right.strip())
        return False

    def parse_block(self, block):
        lines = block.split("\n")
        for line in lines:
            self.parse_line(line)

# Пример использования




interpreter = SimpleLanguage()
interpreter.parse(code)