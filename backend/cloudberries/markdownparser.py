import re

class MarkDownToHtml():

    list_type = None 
    in_code = False

    def __init__(self, text):
        self.text = text

    def iterate(self, text:str) -> str:
        output = ""
        if '\n' in text:
            for idx, line in enumerate(text.split('\n')):
                ending = '\n' if idx < (len(text.split('\n')) - 1) else ''
                stripped = line.lstrip(' ')
                if len(stripped) < 1:
                    continue
                additional, line, parsed = self.__parse_lists(line)
                if additional is not None:
                    output += additional
                if '```' in line:
                    self.in_code = not self.in_code
                    if self.in_code:
                        output += '<pre class=\"parser-code\"><code>'
                    else:
                        output += '</code></pre>\n'
                    continue
                if self.in_code:
                    output += line + '\n'
                    continue
                output += line if parsed else self.parse_line(line) 
                output += ending
        else:
            output = text.lstrip(' ')
            output = self.parse_line(output)
        return output
    
    def __parse_lists(self, line):
        list_type = None
        output_value = None
        stripped = line.lstrip(' ')
        if stripped[0] == '-' or stripped[0] == '+':
            list_type = "<ul class=\"parser-ul\">"
        if stripped[:2] == '1.':
            list_type = "<ol class=\"parser-ol\">"
        if list_type is None:
            if self.list_type is not None:
                output_value =  f"{self.list_type[:1]}/{self.list_type[1:3]}>\n"
                self.list_type = None
            return output_value, line, False
        
        if list_type != self.list_type and self.list_type is not None:
            output_value = f"{self.list_type[:1]}/{self.list_type[1:3]}>\n"
            output_value += list_type
            self.list_type = list_type
        
        if self.list_type is None:
            output_value = list_type + '\n'
            self.list_type = list_type

        prefix =  f"<li class=\"parser-li\">"
        line = f"{prefix}{self.parse_line(' '.join(line.split(' ')[1:]))}</li>"
        return output_value, line, True

    def parse_line(self, line:str) -> str:
        if len(line) < 1:
            return ''
        if line[0] == '#':
            return self.create_heading(line)
        elif '_' in line:
            return self.parse_bold_italic(line)
        else:
            return f"<p class=\"parser-p\">{line}</p>"
        return line
    
    def parse_bold_italic(self, line:str) -> str:
        line = self.__find_replace_helper(line, '__', '<b>')
        line = self.__find_replace_helper(line, '_', '<i>')
        return line
    
    def __find_replace_helper(self, line:str, find:str, replace:str) -> str:
        iterations = 0
        while line.find(find) != -1:
            if iterations % 2 == 0:
                line = re.sub(find, replace, line, 1)
            else:
                line = re.sub(find, replace[:1] + '/' + replace[1:], line, 1)
            iterations += 1
        return line

    def create_heading(self, line:str) -> str:
        weight = 0
        for char in line:
            if char == '#':
                weight += 1
            else:
                break
        text = self.iterate(line[weight:])
        return f"<h{weight} class=\"parser-h{weight}\">{text}</h{weight}>"