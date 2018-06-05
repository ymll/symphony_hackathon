from nlpParser import Parser

parser = Parser()

class Engine:
    def parse(self, question):
        path, parameters = parser.getParseResult(question)
        print(path)
        print(parameters)
        return "done"

