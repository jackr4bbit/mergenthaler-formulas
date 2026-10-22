from mergenthaler import Element, Format, Site
import re
import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.printing.mathml import mathml
from uuid import uuid4

class Formula(Element):
    match = r":{(.*?)}:\n"

    def __init__(self, og: str, equation: sympy.Eq, forms: dict[str, sympy.Eq]):
        self.og = og
        self.equation = equation
        self.forms = forms
        self.id = uuid4()

    def __str__(self) -> str:
        return self.og

    @classmethod
    def parse(cls, text: str, path: Path, feed: parseModule.Feed, formats: list[type[Format]] | None = None) -> Self:
        match = re.match(cls.match, text)

        if match is None:
            raise SyntaxError(f"Unknown formula syntax: {text}.")
        else:
            text = match.group(1).replace(" ", "")

            parts = text.split("=")
            left = parts[0]
            right = parts[1]

            isApprox = left.endswith("~")
            left = left[:-1] if isApprox else left

            symbols = {"E": sympy.Symbol("E"), "I": sympy.Symbol("I")}
            equation = sympy.Eq(parse_expr(left, local_dict=symbols), parse_expr(right, local_dict=symbols))

            return cls(left + ("≈" if isApprox else "=") + right, equation, {str(var): sympy.Eq(var, sympy.solve(equation, var)[0]) for var in equation.free_symbols})

    def html(self, site: Site) -> str:
        def equationToHTML(equation: sympy.Eq) -> str:
            return mathml(equation, printer="presentation")

        def onClick(equation: sympy.Eq) -> str:
            return f"onclick=\"document.getElementById('formula-{self.id}').innerHTML = '{equationToHTML(equation)}'\""

        return f"""<div class="formula">
    <math id="formula-{self.id}" style="cursor: pointer;" {onClick(self.equation)}>{equationToHTML(self.equation)}</math>
    <div style="white-space: pre; font-size: 80%;">Solve for {" ".join(f"<span style=\"box-sizing: content-box; padding: 5px; height: auto; width: max-content; background-color: #BBBBBB; aspect-ratio: 1 / 1; border-radius: 50em; cursor: pointer;\" {onClick(equation)}>{var}</span>" for var, equation in self.forms.items())}</div>
</div>
"""