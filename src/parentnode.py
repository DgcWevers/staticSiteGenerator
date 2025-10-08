from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Error: tag not provided.")
        if self.children == None:
            raise ValueError("Error: children not provided.")
        
        if self.props == None:
            html_text = f"<{self.tag}>"
        else:
            html_text = f"<{self.tag}{self.props_to_html()}>"
        for i in self.children:
            html_text += i.to_html()
        html_text += f"</{self.tag}>"
        return html_text