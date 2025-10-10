from markdown_to_html import markdown_to_html_node
import os


def extract_title(markdown):
    h1 = None
    for line in markdown.split('\n'):
        if line.startswith('# '):
            h1 = line.lstrip('# ')
    if h1 == None:
        raise Exception("Error: no h1 header in markdown!")
    return h1.strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown = file.read()

    with open(template_path, 'r') as file:
        template = file.read()
    
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    title = extract_title(markdown)
    html = replace_title_content(template, title, html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    
    with open(dest_path, 'w') as file:
        file.write(html)

def generate_pages_recursive(dir_path_content, tempate_path, dest_dir_path):
    for i in os.listdir(dir_path_content):
        if i.endswith('.md'):
            html = generate_page(os.path.join(dir_path_content, i), tempate_path, dest_dir_path)
    



def replace_title_content(template, title, html):
    replacements = {
        "{{ Title }}": title,
        "{{ Content }}": html
    }

    for key, value in replacements.items():
        template = template.replace(key, value)

    return template