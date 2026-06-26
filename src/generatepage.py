import os
from markdownconverter import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:        
        with open(from_path, 'r') as file:
            content = file.read()
        with open(template_path, 'r') as file:
            template = file.read()
    except:
        raise Exception("Something went wrong! read")

    Node = markdown_to_html_node(content)
    Nodestring = Node.to_html()

    title = extract_title(content)


    final = template.replace("{{ Title }}", title)
    final = final.replace("{{ Content }}", Nodestring)

    try:
        parent_dir = os.path.dirname(dest_path)

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(dest_path, "w") as f:
         f.write(final)
    except:
        raise Exception("Something went wrong! write")


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating all pages from {dir_path_content} to {dest_dir_path} using {template_path}")
    
    try:
        files_to_gen = crawl_dirs(dir_path_content)

        with open(template_path, 'r') as file:
                template = file.read()

        for files in files_to_gen:
            temp = template
            with open(files, 'r') as file:
                content = file.read()
            
            Node = markdown_to_html_node(content)
            Nodestring = Node.to_html()
            title = extract_title(content)

            final = temp.replace("{{ Title }}", title)
            final = final.replace("{{ Content }}", Nodestring)

            parent_dir = os.path.dirname(files)
            parent_dir = parent_dir.replace(dir_path_content, dest_dir_path)

            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            with open(os.path.join(parent_dir, os.path.basename(files.replace(".md", ".html"))), "w") as f:
                 f.write(final)
            


    except:
        raise Exception("Something went wrong! recursive")     

def crawl_dirs(dir_path_content):

    md_files = []

    for item in os.listdir(dir_path_content):
        fullpath = os.path.join(dir_path_content, item)
        if os.path.isfile(fullpath):
            if item.endswith(".md"):
                md_files.append(fullpath)
        else:
            md_files.extend(crawl_dirs(fullpath))

    return md_files

            

            
    