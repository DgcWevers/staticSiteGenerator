
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    # def to_html(self):
    #     if self.tag == None:
    #         raise ValueError("Error: tag not provided.")
    #     #if self.children == None:
    #     #    raise ValueError("Error: children not provided.")
        
    #     if self.props == None:
    #         html_text = f"<{self.tag}>"
    #     else:
    #         html_text = f"<{self.tag}{self.props_to_html()}>"
    #     if self.children != None:
    #         for i in self.children:
    #             html_text += i.to_html()
    #     html_text += f"</{self.tag}>"
    #     return html_text
    
    # def props_to_html(self):
    #     result_str = ""
    #     for key,value in self.props.items(): 
    #         result_str += f' {key}="{value}"'
    #     return result_str

    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode with tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"
                

    # def __eq__(self, other):
    #     if (self.tag == other.tag) & \
    #         (self.value == other.value) & \
    #         (self.children == other.children) & \
    #         (self.props == other.props):
    #         return True
    #     else:
    #         return False