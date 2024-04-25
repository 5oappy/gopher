#parser_1.py

class Parser:
    def __init__(self, input_text):
        # self.filter = filter
        self.input = input_text
        
    def parse_response(self):
        lines = self.input.split('\n')
        options = []
        for line in lines:
            if line.startswith('0') or line.startswith('1'):
                parts = line.split('\t')
                if len(parts) >= 4:
                    option = self.parse_option(parts)
                    options.append(option)
                    
        return options

    def parse_option(self, parts):
        option_type = parts[0][0]
        name = parts[0].strip()
        selector = parts[1].strip()
        host = parts[2].strip()
        port = parts[3].strip()
        option = {'type': option_type, 'name': name, 'selector': selector, 'host': host, 'port': port}
        return option
        
    def extract_paths(self):
        paths = []
        for line in self.input.split('\n'):
            if line.startswith('0') or line.startswith('1'):
                parts = line.split('\t')
                path = parts[1].strip()
                paths.append(path)
        return paths
