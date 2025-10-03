from textnode import TextNode # type: ignore

def main():
    textnode = TextNode(text="This is some anchor text", text_type="link", url="https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()