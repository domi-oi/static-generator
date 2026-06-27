from textnode import TextNode, TextType
from copystatic import movefiles
from generatepage import generate_page, generate_page_recursive
import sys

print("hello world")


def main(basepath):
    
    movefiles()
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_page_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except:
        print("Wrong Format!")