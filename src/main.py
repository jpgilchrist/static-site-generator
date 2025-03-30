from textnode import TextNode, TextType


def main():
    text_node = TextNode("this is some text", TextType.LINK, "https://boot.dev")
    print(text_node)


if __name__ == "__main__":
    main()
