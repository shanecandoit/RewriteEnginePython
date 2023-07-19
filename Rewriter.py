
from dataclasses import dataclass
import re
from typing import List, Tuple, Dict


def find_variables(text: str) -> List[str]:
    found = re.findall('([a-zA-Z\d]+:)', text)
    # print(found)
    return found


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
        print(f'vleft: {vleft}, vright: {vright}')
        both = sorted(set(vleft + vright))
        self.variables = both


class Rewriter:
    """ Rewrite an """
    rules = []
    source = ''

    def __init__(self, rules, source):
        self.rules = rules
        self.source = source

    def __call__(self):
        return self.rewrite()

    @staticmethod
    def line_word_vars(line: str) -> list:
        """ take a list like add(a:, b:) and 
            return a list of the variables like ['a:', 'b:']"""
        line = line.replace('(', ' ( ').replace(')', ' ) ').replace(
            ',', ' , ').replace(':', ': ')
        words = line.split(' ')
        words = [word for word in words if word.endswith(':')]
        return words

    @staticmethod
    def line_word_funcs(line: str) -> list:
        """ take a list like add(a:, b:) and return a list of the variables like ['add(']"""
        line = line.replace('(', '( ').replace(')', ' ) ').replace(',', ' , ')
        words = line.split(' ')
        print(words)
        words = [word for word in words if word.endswith('(')]
        print(words)
        return words

    @staticmethod
    def make_regexp(func_name: str, args: list) -> str:
        """ make a functional style regex, with name and args like: name(arg1, arg2)
        s = make_regexp('add', ['a', 'b'])
        assert s == 'add\(((?P<a>\w+), ((?P<b>\w+)\)'
        """
        r = func_name
        r += '\('
        for arg in args:
            r += f'((?P<{arg}>\w+), '
        r = r[:-2]
        print(r)
        r += '\)'
        return r

    def rewrite(self):
        print('rewrite')
        self.rule_pairs = [rule.split('->') for rule in self.rules]
        result = ''
        for line in self.source.split('\n'):
            for rule_in, rule_out in self.rule_pairs:

                print(f'rule_in: {rule_in}, rule_out: {rule_out}')
                # rule_in: add(a:, b:) , rule_out:  add(a:+1, b:-1)

                rule_in_vars = self.line_word_vars(rule_in)
                # ['a:', 'b:']
                rule_out_vars = self.line_word_vars(rule_out)
                # ['a:', 'b:']
                rule_in_funcs = self.line_word_funcs(rule_in)
                # ['add(']
                rule_out_funcs = self.line_word_funcs(rule_in)
                # ['add(']

                # regex to match rule_in
                # re.search('(?P<name>.*) (?P<phone>.*)', 'John 123456')
                # import re
                # r = re.search('add\((?P<first>\w+), (?P<second>\w+)\)', 'add(2, 3)')
                # print(r) # <re.Match object; span=(0, 9), match='add(2, 3)'>
                # print(r.group('first')) # 2
                # print(r.group('second')) # 3
                func_name = rule_in_funcs[0].replace('(', '')
                # 'add'
                rule_in_regex = self.make_regexp(func_name, rule_in_vars)
                print(f'rule_in_regex {rule_in_regex}')
                # rule_in_regex add\(((?P<a:>\w+), ((?P<b:>\w+)\)

                # how to match rule_in to line?
                # if rule_in_funcs[0] in line:
                if re.search(rule_in_regex, line):
                    print(f'found {rule_in_regex} in {line}')

                    # bind vars
                    # a: 3
                    # b: 2
                    # add(a:, b:)
                    # add(a:+1, b:-1)
                    replace_out = rule_out

                    line = line.replace(rule_in, rule_out)
        # self.source = result
        return result

    def __repr__(self):
        return f'Rewriter(rules:{self.rules}, source:{self.source})'


if __name__ == '__main__':
    wr = Rewriter([], 'Hello {name}')
    print(wr)

    # rule 1
    r1_rec = 'add(a:, b:) -> add(a:+1, b:-1)'
    r1_base = 'add(a:, 0) -> a:'

    wr.rules.append(r1_rec)
    wr.rules.append(r1_base)
    print(wr)

    s = 'add(3,2)'
    wr.source = s
    print(wr)

    wr.rewrite()
    print(wr)
