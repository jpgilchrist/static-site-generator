import os
import re
import shutil

from blocks_markdown import markdown_to_html_node


def extract_title(markdown):
    titles = re.findall(r"^# (.*)$", markdown, re.MULTILINE)
    if len(titles) == 0:
        raise Exception("No title found in markdown")
    return titles[0]


def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page {from_path} -> {dest_path} using {template_path} ({base_path})")

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    with open(from_path, "r") as markdown_file:
        markdown = markdown_file.read()

        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

        with open(template_path, "r") as template_file:
            template = template_file.read()

            html = template.replace("{{ Title }}", title)
            html = html.replace("{{ Content }}", content)
            html = html.replace('href="/', f'href="{base_path}')

            dest_file_name = str(os.path.basename(from_path).replace(".md", ".html"))
            if not os.path.exists(os.path.join(dest_path, dest_file_name)):
                with open(os.path.join(dest_path, dest_file_name), "w") as dest_file:
                    dest_file.write(html)


def generate_all(src_path, dest_path, template_path="./template.html", base_path="/"):
    if not os.path.exists(src_path):
        raise Exception("Source directory does not exist", src_path)

    if os.path.isdir(src_path) and not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for item in os.listdir(src_path):
        item_src_path = os.path.join(src_path, item)
        item_dest_path = os.path.join(dest_path, item)
        if os.path.isdir(item_src_path):
            generate_all(item_src_path, item_dest_path, base_path=base_path)
        else:
            if item.endswith(".md"):
                generate_page(item_src_path, template_path, dest_path, base_path=base_path)


def copy_all(src, dest):
    if not os.path.exists(src):
        raise Exception("Source directory does not exist", src)

    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_all(s, d)
        else:
            shutil.copy(s, d)
