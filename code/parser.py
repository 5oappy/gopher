#parser_1.py

class Parser:
    def __init__(self, input_text):
        # self.filter = filter
        self.input = input_text
        
    def parse_response(self):
        print("Reached parser")
        lines = self.input.split('\n')
      
        options = []
        print("start loop")
        for line in lines:
            if line.startswith('0') or line.startswith('1'):
                parts = line.split('\t')
                if len(parts) >= 4:
                    option = self.parse_option(parts)
                    options.append(option)
                # print("Option:", option)
        return options

    def parse_option(self, parts):
        option_type = parts[0][0]
        # print(parts[0][0])
        name = parts[0].strip()
        # print(parts[0])
        selector = parts[1].strip()
        # print(parts[1])
        host = parts[2].strip()
        # print(parts[2])
        port = parts[3].strip()
        # print(parts[3])
        option = {'type': option_type, 'name': name, 'selector': selector, 'host': host, 'port': port}
        # print(option)
        return option
        
    def extract_paths(self):
        paths = []
        for line in self.input.split('\n'):
            if line.startswith('0') or line.startswith('1'):
                parts = line.split('\t')
                path = parts[1].strip()
                paths.append(path)
        return paths
