

from dataclasses import dataclass
import re
from typing import List, Tuple, Dict

rules_text = '''
add(a:, b:) -> add(a:+1, b:-1)
add(a:,0)   -> a:
add(0,b:)   -> b:'''


@dataclass
class Rule:
    left: str
    right: str
    variables: List[str]

    def __init__(self, left, right):
        self.left = left
        self.right = right
        vleft = find_variables(self.left)
        vright = find_variables(self.right)
        # print(f'vleft: {vleft}, vright: {vright}')
        both = sorted(set(vleft + vright))
        self.variables = both


def find_variables(text: str) -> List[str]:
    found = re.findall(r'([a-zA-Z\d]+:)', text)
    # print(found)
    return found


def rule_match(rules: List[Rule], text: str) -> Tuple[Rule, Dict[str, str]]:
    """ Which left hand rule matches the text?
    text like 'add(3, 2)'
    """
    for rule in rules:
        # TODO better than this
        variables = find_variables(rule.left)
        regex_string = rule.left.replace('(', '\(').replace(')', '\)')
        for var in variables:
            regex_string = regex_string.replace(
                var,
                '(?P<{}>.*)'.format(var[:-1]))
        # regex_from_rule = rule.left.replace('', '')
        match = re.match(regex_string, text)
        if match:
            return rule, match.groupdict()
    return None, None


def math_eval(text: str) -> str:
    """ Evaluate text like '3+1' to '4'
        and eval_expr('1 + 2*3**(4^5) / (6 + -7)') to -5.0
    """
    result = text[:]  # copy
    if '(' in text:
        # pass
        inner_expr = ''
        first_close = text.find(')')
        last_open = text.rfind('(')
        inner = text[last_open+1: first_close]  # remove ()
        inner_expr = math_eval(inner)
        result = text[:last_open+1] + inner_expr + text[first_close:]
    else:

        # power
        # regex_pow = re.compile(r'(\d+)(\*\*)(\d+)')
        # pow = regex_pow.search(text)
        # if pow:
        #     inner_expr = math_eval(pow)
        #     result = regex_pow.sub(r'\1 \2 \3', inner_expr)

        # multiply and divide
        regex_mult = re.compile(r'(\d+)(\*|\/)(\d+)')
        mul_div = regex_mult.search(text)
        if mul_div:
            match = result[mul_div.start(1):mul_div.end(3)]
            inner_res = str(eval(match))
            result = result.replace(match, inner_res)

            # dont fall into addition, may have more mults to do
            if len(result) < len(text):
                result = math_eval(result)
            return result

        # add and subtract
        regex_add_sub = re.compile(r'(\d+)(\+|-)(\d+)')
        add_sub = regex_add_sub.search(text)
        if add_sub:
            match = result[add_sub.start(1): add_sub.end(3)]
            inner_expr = add_sub.string
            inner_res = str(eval(match))
            result = text.replace(match, inner_res)

            if len(result) < len(text):
                result = math_eval(result)
            return result

    if result == text:
        return result

    return result


if __name__ == '__main__':

    a = math_eval('3+1')
    assert a == '4'

    b = math_eval('4*5-2*3')  # 20 - 6
    assert b == '14'

    rules = []
    for line in rules_text.split('\n'):
        if line:
            left, right = line.split('->')
            # print(f'left {left}, right {right}')
            left = left.strip()
            right = right.strip()
            # print(f'left {left}, right {right}')
            rules.append(Rule(left, right))
            # print(f'rules = {rules}')
    print(f'rules {rules}')

    sample = 'add(3, 2)'
    print(f'sample {sample}')

    which_rule, var_match = rule_match(rules, sample)
    #
    print(f'which_rule {which_rule}')
    # which_rule Rule(left='add(a:, b:)', right='add(a:+1, b:-1)', variables=['a:', 'b:'])
    print(f'var_match {var_match}')
    # var_match {'a': '3', 'b': '2'}

    substitution = which_rule.right
    for name, value in var_match.items():
        name = name + ':'  # 'a' -> 'a:'
        substitution = substitution.replace(name, value)
    print(f'substitution {substitution}')
    # substitution add(3+1, 2-1)

    evald = math_eval(substitution)
    print(f'evald {evald}')
    # evald add(3+1, 2-1)
    assert evald == 'add(4, 1)'
