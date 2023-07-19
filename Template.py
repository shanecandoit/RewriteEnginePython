

class Template:
    """ Template Engine using Python's str.format() method. """

    def __init__(self, template):
        self.template = template

    def render(self, **kwargs):
        return self.template.format(**kwargs)


def main():
    template = Template('Hello {name}')
    print(template.render(name='World'))


if __name__ == '__main__':
    main()
