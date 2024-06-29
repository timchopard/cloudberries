import re
import markdown

def _get_footnotes(text:str):
    text_copy = text
    regex_tag = re.compile(r"[\w]+[_\-\d\w]*")
    regex_foot = re.compile(r"\]:.+")

    footer_dict = {}

    for footer in re.findall(r"[\[]\^[\w\d]+[_\-\w\d]*[\]]:.+", text):
        tag = re.search(regex_tag, footer).group(0)
        footnote = re.search(regex_foot, footer).group(0)[2:].lstrip()
        new_foot = f"{footnote} <a id='{tag}-foot' href='#{tag}'>"
        new_foot += "&#10548</a>"
        text_copy = text_copy.replace(footer, '')
        footer_dict[tag] = new_foot

    text_copy = text_copy.rstrip() + '\n'
    text = text_copy
    
    for ii, note in enumerate(re.findall(r"[\[]\^[\w\d]+[_\-\w\d]*[\]]", text)):
        tag = re.search(regex_tag, note).group(0)
        new_note = f"<sup><a id='{tag}' href='#{tag}-foot'>[{ii + 1}]</a></sup>"
        text_copy = text_copy.replace(note, new_note)
        if tag in footer_dict.keys():
            text_copy += '\n' 
            text_copy += f"<p><small>{ii + 1}. {footer_dict[tag]}</small></p>"
        else:
            text_copy += '\n' + f"{ii + 1}. ! Missing or misspelled reference !"

    return text_copy


def full_parse(text:str):
    text = markdown.markdown(_get_footnotes(text))
    text = text.replace('<code>', '<pre><code class="hljs">')
    text = text.replace('</code>', '</code></pre>') 
    return text