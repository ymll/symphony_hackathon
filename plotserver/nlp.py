from nlpParser import Parser

parser = Parser()

class Engine:
    def parse(self, question):
        path, parameters = parser.getRoutingPath(question)
        print(path)
        print(parameters)
        return "done"

