from textnode import TextNode, TextType

def main():
    example_text_node = TextNode("anchor text", TextType.LINK, "https://www.boot.dev")
    print(example_text_node)

if __name__ == "__main__":
    main()