from textnode import TextNode, TextType
from copystatic import movefiles
from generatepage import generate_page, generate_page_recursive

print("hello world")


def main():
    
    movefiles()
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_page_recursive("content", "template.html", "public")

main()