from functools import reduce
from operator import add

class Element:
    
    def __init__(self, value, var="x"):
        self.coeff, self.pow = list(map(int, value.split(var + "^")))
        self.var = var

    def __repr__(self):
        return str(self.coeff) + self.var + "^" + str(self.pow)
    
    def __add__(self, element):
        if self.pow == element.pow:
            new_el = Element(str(self), var=self.var)
            new_el.coeff += element.coeff
            return new_el
        raise Exception

    def __neg__(self):
        new_el = Element(str(self), var=self.var)
        new_el.coeff = -self.coeff
        return new_el

    def __sub__(self, element):
        return self + (-element)
    
    def __mul__(self, element):
        new_el = Element(str(self), var=self.var)
        new_el.coeff *= element.coeff
        new_el.pow += element.pow
        return new_el
    
    def __floordiv__(self, element):
        new_el = Element(str(self), var=self.var)
        new_el.coeff //= element.coeff
        new_el.pow -= element.pow
        return new_el
    
    def beaty_repr(self, show_sign=True):
        if self.coeff == 0:
            return ""

        s = []
        if self.coeff > 0:
            if show_sign:
                s.append("+")
            if self.coeff != 1 or self.pow == 0:
                s.append(str(self.coeff))
        elif self.coeff < 0:
            if self.coeff == -1:
                s.append("-")
            else:
                s.append(str(self.coeff))
        
        if self.pow != 0:
            s.append(self.var)
            if self.pow != 1:
                s.append("^" + str(self.pow))
        
        return "".join(s)
        


class Expression:
    
    def __init__(self, expression, var="x"):
        self.var = var
        self.value = self.convert(expression)
    
    def convert(self, expression):
        new_expr = list(expression.translate(str.maketrans("", "", " ")))

        idx = 0
        while idx < len(new_expr):
            if new_expr[idx] == "^":
                idx += 1
                start = True
                while idx < len(new_expr) and (new_expr[idx].isdigit() or (new_expr[idx] == "-" and start)):
                    if start:
                        start = False
                    idx += 1
                
                if idx == len(new_expr):
                    break

            if new_expr[idx] == "-" and idx != 0 and new_expr[idx-1] not in ("/", "*"):
                new_expr.insert(idx, "+")
                idx += 1
            elif new_expr[idx] == self.var:
                add_idx = 0
                if idx == len(new_expr) - 1 or new_expr[idx+1] != "^":
                    new_expr.insert(idx+1, "^1")
                    add_idx += 1
                if idx == 0 or not new_expr[idx-1].isdigit():
                    new_expr.insert(idx, "1")
                    add_idx += 1
                idx += add_idx
            elif new_expr[idx].isdigit():
                while idx < len(new_expr) and new_expr[idx].isdigit():
                    idx += 1
                idx -= 1
                
                if idx == len(new_expr) - 1 or new_expr[idx+1] != self.var:
                    new_expr.insert(idx+1, self.var + "^0")
                    idx += 1
            
            idx += 1

        return "".join(new_expr)
    
    def eval(self):
        def convert_to_element(term):
            if "*" in term or "//" in term:
                for idx in range(len(term) - 1, -1, -1):
                    if term[idx] == "*":
                        return convert_to_element(term[0:idx]) * Element(term[idx+1:], var=self.var)
                    elif term[idx] == "/":
                        return convert_to_element(term[0:idx-1]) // Element(term[idx+1:], var=self.var)

            return Element(term, var=self.var)
        
        if len(self.value) == 0:
            return "0"

        self.value = list(map(convert_to_element, self.value.split("+")))
        self.value = sorted(self.value, key=lambda el: el.pow, reverse=True)

        new_value = []
        p1, p2 = 0, 0
        while p1 < len(self.value) and p2 < len(self.value):
            if self.value[p1].pow != self.value[p2].pow:
                new_value.append(reduce(add, self.value[p1:p2]))
                p1 = p2
            p2 += 1
        new_value.append(reduce(add, self.value[p1:p2]))
        self.value = new_value

        self.value = "".join([el.beaty_repr() for el in self.value])
        if len(self.value) == 0:
            return "0"
        elif self.value[0] == "+":
            self.value = self.value[1:]
        return self.value


def identify_var(expression):
    acceptable_vars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    for var in acceptable_vars:
        if var in expression:
            return var
    
    return "x"


def simplify(expression, auto_identify_var=False, variable="x"):
    """You can either pass the variable, which is used in expression,
       or you can force the function to identify the variable automatically
       (change auto_identify_var to True)"""
    
    if not auto_identify_var:
        var = variable
    else:
        var = identify_var(expression)
    
    return Expression(expression, var=var).eval()


def auto_simplify(expression):
    """Simplify the expression (variable will be identified automatically)"""
    return simplify(expression, auto_identify_var=True)