
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result_str = ""
        for key,value in self.props.items(): 
            result_str += f' {key}="{value}"'
        return result_str

    def __repr__(self):
        return f"HTMLNode with tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"
                