from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_notes = []

    def tonewnodes(node, delimiter, text_type):
        new_note = []
        if node.text_type != TextType.TEXT:
            return [node]
        if delimiter not in node.text:
            return [node]
            #raise Exception(f"Error: delimiter not found in text")
        else:
            texts = node.text.split(delimiter)
            if len(texts) < 3:
                return [node]
            new_note.append(TextNode(texts[0], TextType.TEXT))
            new_note.append(TextNode(texts[1], text_type))
            new_note.append(TextNode(texts[2], TextType.TEXT))
        return new_note
    
    for node in old_nodes:
        try:
            new_notes.extend(tonewnodes(node, delimiter, text_type))
        except Exception:
            new_notes.extend(node)
    
    return new_notes



def extract_markdown_images(text):
    result = []
    img_texts = re.findall(r'\!\[(.*?)\]', text)
    img_links = re.findall(r'\!\[.*?\]\((.*?)\)', text)
    for i in range(0,len(img_texts)):
        result.append((img_texts[i], img_links[i]))
    return result

def extract_markdown_links(text):
    result = []
    link_texts = re.findall(r'\[(.*?)\]', text) # r'[^!]\[(.*?)\]'
    link_links = re.findall(r'\[.*?\]\((.*?)\)', text) # r'[^!]\[.*?\]\((.*?)\)'
    for i in range(0,len(link_texts)):
        result.append((link_texts[i], link_links[i]))
    return result

def split_nodes_image(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        try:
            images = re.findall(r'(\!\[.*?\]\(.*?\))', node.text)
            text = node.text.split(images[0])
            for i in range(1, len(images)):
                new_text = text[0:i]
                new_text.extend(text[i].split(images[i]))
                text = new_text

            new_nodes = []
            if node.text.startswith('!'):
                for i in range(0, len(images)):
                    image = extract_markdown_images(images[i])
                    if image:
                        new_nodes.append(TextNode(image[0][0], TextType.IMAGE, image[0][1]))
                    if i < len(text):
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
            else:
                for i in range(0, len(images)):
                    image = extract_markdown_images(images[i])
                    if i < len(text):
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
                    if image:
                        new_nodes.append(TextNode(image[0][0], TextType.IMAGE, image[0][1]))
                if (len(text) > len(images)) and (text[-1] != ''):
                    new_nodes.append(TextNode(text[-1], TextType.TEXT))
            new_nodes_list.extend(new_nodes)
        except IndexError: 
            new_nodes_list.append(node)
        except TypeError:
            new_nodes_list.append(node)

    return new_nodes_list


def split_nodes_link(old_nodes):
    new_nodes_list = []
    for node in old_nodes:
        try:
            links = re.findall(r'(\[.*?\]\(.*?\))', node.text)
            text = node.text.split(links[0])
            for i in range(1, len(links)):
                new_text = text[0:i]
                new_text.extend(text[i].split(links[i]))
                text = new_text

            new_nodes = []
            if node.text.startswith('['):
                for i in range(0, len(links)):
                    link = extract_markdown_links(links[i])
                    if link:
                        new_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))
                    if i < len(text):
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
            else:
                for i in range(0, len(links)):
                    link = extract_markdown_links(links[i])
                    if i < len(text):
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
                    if link:
                        new_nodes.append(TextNode(link[0][0], TextType.LINK, link[0][1]))
                if (len(text) > len(links)) and (text[-1] != ''):
                    new_nodes.append(TextNode(text[-1], TextType.TEXT))
            new_nodes_list.extend(new_nodes)
        except IndexError: 
            new_nodes_list.append(node)
        except TypeError:
            new_nodes_list.append(node)

    return new_nodes_list


def text_to_textnodes(text):
    nodes_list = [TextNode(text, TextType.TEXT)]
    def check_state(nodes_list):
        # fix early return and use 'or' (not |)
        for i in nodes_list:
            if i.text_type == TextType.TEXT and (('**' in i.text) or ('_' in i.text) or ('`' in i.text)):
                return True
        return False
    state = check_state(nodes_list)
    while state:
        for key, value in {'**':TextType.BOLD, '_':TextType.ITALIC, '`':TextType.CODE}.items():
            try:
                nodes_list = split_nodes_delimiter(nodes_list, key, value)
            except Exception:
                pass
        state = check_state(nodes_list)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)
    return nodes_list