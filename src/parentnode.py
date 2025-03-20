from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('tag is required')
        if type(self.children) != list:
            raise ValueError('children should be a list')
        if len(self.children) == 0:
            raise ValueError('children should not be empty')
        
        output = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            output += child.to_html()
        output += f'</{self.tag}>'
        
        return output