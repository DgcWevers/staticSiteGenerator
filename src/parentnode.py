# python
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("ParentNode requires a tag")
        # normalize children to a list
        if children is None:
            raise ValueError("ParentNode requires children")
        if not isinstance(children, (list, tuple)):
            children = [children]
        super().__init__(tag, None, children, props)

    # def to_html(self):
    #     if not self.tag:
    #         raise ValueError("ParentNode requires a tag")
    #     if not self.children:
    #         raise ValueError("ParentNode requires children")
    #     open_tag = f"<{self.tag}{self.props_to_html()}>"
    #     inner = "".join(child.to_html() for child in self.children)
    #     close = f"</{self.tag}>"
    #     return f"{open_tag}{inner}{close}"

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode requires a tag")
        if self.children is None:
            raise ValueError("ParentNode requires children")
        open_tag = f"<{self.tag}{self.props_to_html()}>"
        inner = "".join(child.to_html() for child in self.children)
        return f"{open_tag}{inner}</{self.tag}>"