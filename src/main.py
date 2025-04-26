from textnode import (
    TextNode,
    TextType,
)


def main():
    node = TextNode("Testing 123", TextType.NORMAL)
    print(node)


if __name__ == "__main__":
    main()
