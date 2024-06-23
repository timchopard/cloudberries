import re

class MarkdownToHTML():

    __footnotes = []
    __in_footnotes = False
    __list = None 
    __make_contents = False
    __add_classes = False

    def __init__(self):
        pass

    def handle_bold_italic(self, in_string:str):
        for identifier_set in [
            {
                "regex": r"\*\*[^\*$]+\*\*|__[^_$]+__",
                "chars": '__',
                "alt"  : '**',
                "html0": '<b>',
                "html1": '</b>',
            },
            {
                "regex": r"\*[^\*$]+\*|_[^_$]+_",
                "chars": '_',
                "alt"  : '*',
                "html0": '<i>',
                "html1": '</i>',
            },
        ]:
            in_string = self.__bold_italic_helper(in_string, identifier_set)
        return in_string

    def __bold_italic_helper(self, in_string:str, identifiers:dict):
        examples = re.findall(identifiers["regex"], in_string)
        for ex in examples:
            copy = ex 
            ex = ex.replace(identifiers["chars"], identifiers["html0"], 1)
            ex = ex.replace(identifiers["chars"], identifiers["html1"], 1)
            ex = ex.replace(identifiers["alt"], identifiers["html0"], 1)
            ex = ex.replace(identifiers["alt"], identifiers["html1"], 1)
            in_string = in_string.replace(copy, ex)
        return in_string

    def handle_titles(self, in_string:str):
        title_depth = 0
        while len(in_string) > title_depth and in_string[title_depth] == '#':
            title_depth += 1
        if title_depth == 0:
            return in_string
        in_string = f"<h{title_depth}>{in_string[title_depth:].lstrip()}"
        return in_string + f'</h{title_depth}>'

    def handle_footnotes(self, in_string:str):
        # Find footnote texts
        footnotes = re.findall(r"\[\^[\w\d]+\]:", in_string)
        if len(footnotes) == 1:
            prefix = ""
            if not self.__in_footnotes:
                prefix += "<hr><ul><small>\n"
                self.__in_footnotes = True

            in_string = in_string.replace(footnotes[0], '').lstrip()
            footnote = footnotes[0][2:-2]
            if footnote in self.__footnotes:
                prefix += f"<li><a id='{footnote}-foot'>" 
                prefix += f"{self.__footnotes.index(footnote) + 1}.</a> " 
                suffix = f" <a href='#{footnote}'>^</a></li>"
                return prefix + in_string + suffix

        if self.__in_footnotes and len(footnotes) < 1:
            self.__in_footnotes = False 
            in_string = "</small></ul>\n" + in_string

        # Find all footnote links
        footnotes = re.findall(r"\[\^[\w\d]+\]", in_string)
        for footnote in footnotes:
            identifier = footnote[2:-1]
            if identifier not in self.__footnotes:
                self.__footnotes.append(identifier)
            link_string = f"<a id='{identifier}' href='#{identifier}-foot'>"
            link_string += f"[{self.__footnotes.index(identifier) + 1}]</a>"
            in_string = in_string.replace(footnote, f"<sup>{link_string}</sup>")
        
        return in_string

    def handle_lists(self, in_string:str):
        prefix = ""
        if in_string.lstrip()[0] in ['+', '-']:
            if self.__list is None:
                self.__list = 'ul'
                prefix = '<ul>\n'
            elif self.__list == 'ol':
                self.__list = 'ul'
                prefix = '</ol><ul>\n'
            in_string = f"<li>{in_string.lstrip()[1:].lstrip()}</li>"
        elif self.__list == 'ul':
            prefix = '</ul>'
            self.__list == None 
        if in_string.lstrip()[:2] == '1.':
            if self.__list is None:
                prefix += '<ol>'
                self.__list = 'ol'
            in_string = f"<li>{in_string.lstrip()[2:].lstrip()}</li>"
        elif self.__list == 'ol':
            prefix = '</ol>' + prefix
        return prefix + in_string

    def is_comment(self, line):
        return len(line) > 7 and line[:4] == '<!--' and line[-3:] == '-->'

    def line_by_line(self, in_string:str):
        in_list = in_string.split('\n')
        if self.is_comment(in_list[0]):
            instructions = in_list[0].split(' ')
            if 'mkcon' in instructions:
                self.__make_contents = True
            if 'addcls' in instructions:
                self.__add_classes = True

        out_list = []
        for item in in_list:
            if self.is_comment(item):
                continue
            if len(item.lstrip()) < 1:
                continue
            item = self.handle_titles(item)
            item = self.handle_lists(item)
            item = self.handle_footnotes(item)
            out_list.append(self.handle_bold_italic(item))

        if self.__in_footnotes or self.__list == 'ul':
            out_list.append(f'{"</small" if self.__in_footnotes else ""}</ul>')
            self.__in_footnotes = False 
            self.__list = None
        if self.__list == 'ol':
            out_list.append('</ol>')
            self.__list = None
        return '\n'.join(out_list)

    def __manage_classes(self, text:str):
        if not self.__add_classes: return text
        print("adding classes")
        for tag in ['h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'code']:
            print(text.find(f'<{tag}'))
            text = text.replace(f'<{tag}', f'<{tag} class="parser-{tag}" ')
        text = text.replace('<pre', '<pre class="parser-code" ')
        text = text.replace(
            '<code', 
            '<code class="hljs language-python" data-highlighted="yes" '
        )

        return text
    
    def __manage_contents(self, text:str):
        return text

    def split_text(self, in_string:str):
        text_list = in_string.split('```')
        new_list = []
        for idx, text in enumerate(text_list):
            if idx % 2:
                new_list.append(f"<pre><code>{text}</code></pre>")
            else:
                new_list.append(self.line_by_line(text))

        full_text = '\n'.join(new_list)
        full_text = self.__manage_classes(full_text)
        full_text = self.__manage_contents(full_text)

        return full_text

 