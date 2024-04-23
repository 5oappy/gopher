#parser_1.py

class Parser:
    def __init__(self, input_text):
        # self.filter = filter
        self.input = input_text
        

    def parse(self):
        pass

    # def filter_invalid_lines(self):
    #     filtered_lines = [line for line in self.input.split('\n') if "invalid 0" not in line]
    #     return '\n'.join(filtered_lines)
    
    # def parse_item(self, item_line):
    #     item_type = item_line[0]
    #     description = item_line[1:-1].strip()
    #     selector, host, port = item_line.split('\t')[-3:]
    #     return GopherItem(item_type, description, selector, host, int(port))
    
    def parse_response(self):
        print("Reached parser")
        lines = self.input.split('\n')
        options = []
        print("splited")
        for line in lines:
            print("starting new line")
            parts = line.split('\t')
            if len(parts) >= 5:
                option_type = parts[0]
                name = parts[1]
                selector = parts[2]
                host = parts[3]
                port = parts[4]
                options.append({'type': option_type, 'name': name, 'selector': selector, 'host': host, 'port': port})
                print("Option:", options)
        return options


    
    def extract_paths(self):
        paths = []
        for line in self.input.split('\n'):
            if line.startswith('0') or line.startswith('1'):
                parts = line.split('\t')
                path = parts[1].strip()
                paths.append(path)
        return paths
