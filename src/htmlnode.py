class HTMLNode():
    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict[str, str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

#    def props_to_html(self):
#        if self.props:
#            PropValues = " "
#            for prop in self.props:
#                PropValues += f'"{prop}={self.props[prop]}"'
#            return PropValues
#        return ""

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f" HTMLNODE TAG: {self.tag} VALUE: {self.value} CHILDREN: {self.children} PROPS: {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value!")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LEAFNODE TAG: {self.tag} VALUE: {self.value} PROPS: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode],  props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("all parent nodes must have a value!")
        if self.children == None or len(self.children) == 0:
            raise ValueError("all parent nodes must have children!")
        htmltext = ""
        for child in self.children:
            htmltext += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{htmltext}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode TAG: {self.tag}, CHILDREN: {self.children} PROPS: {self.props}"