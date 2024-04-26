#parser_1.py

class Parser:
    def __init__(self, input_text, client_instance):
        self.input = input_text
        # self.client_instance = client_instance
        
    def parse_response(self):
        lines = self.input.split('\n')
        
        options = []
        for line in lines:
            parts = line.split('\t')

            if line.startswith('0') or line.startswith('1') or line.startswith ('9'):
                if len(parts) >= 4:
                    option = self.parse_option(parts)
                    options.append(option)
            elif line.startswith('2'):
                #item is cso phonebook server
                pass

            elif line.startswith('3'):
                # self.client_instance.stats.add_invalid_references()
                return None
            elif line.startswith('4'):
                # binhexed Macintosh file
                pass
            elif line.startswith('5'):
                #DOS archive that will keep sending as long as client allows
                pass
            elif line.startswith('6'):
                # UNIX unencoded file
                pass
            elif line.startswith('7'):
                # Index-Search server
                pass
            elif line.startswith('8'):
                # points to text based telnet session
                pass
            
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
