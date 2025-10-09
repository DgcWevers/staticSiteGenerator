from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_notes = []

    def tonewnodes(node, delimiter, text_type):
        if node.text_type != TextType.TEXT:
            new_notes.append(node)
        if delimiter not in node.text:
            print(delimiter)
            print(node.text)
            raise Exception(f"Error: delimiter not found in text")
        else:
            texts = node.text.split(delimiter)
        new_note = []
        new_note.append(TextNode(texts[0], TextType.TEXT))
        new_note.append(TextNode(texts[1], text_type))
        new_note.append(TextNode(texts[2], TextType.TEXT))
        return new_note
    
    if len(old_nodes) > 1:
        for node in old_nodes:
            new_notes.append(tonewnodes(node, delimiter, text_type))
    else:
        new_notes = tonewnodes(old_nodes[0], delimiter, text_type)
    
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
    link_texts = re.findall(r'[^!]\[(.*?)\]', text)
    link_links = re.findall(r'[^!]\[.*?\]\((.*?)\)', text)
    for i in range(0,len(link_texts)):
        result.append((link_texts[i], link_links[i]))
    return result