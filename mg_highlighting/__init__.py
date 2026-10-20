from mergenthaler import Format, Site

class Highlight(Format):
    name = "highlight"
    start = r"\[\*([^\n]*?): "
    end = r"\*\]"

    def html(self, site: Site) -> str:
        print(self.groups)
        if inputColor := self.groups.get(1):
            if color := site.colors.get(inputColor):
                return f"<mark style=\"background-color: {color.hex}\">{self.text.html(site, noFormat=True)}</mark>"
            else:
                return f"<mark>{inputColor}: {self.text.html(site, noFormat=True)}</mark>"
        else:
            return f"<mark>{self.text.html(site, noFormat=True)}</mark>"
