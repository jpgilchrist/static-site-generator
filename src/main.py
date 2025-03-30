from textnode import TextNode, TextType
import os
import shutil


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


def build():
    shutil.rmtree("public", ignore_errors=True)
    copy_all("static", "public")


def main():
    build()


if __name__ == "__main__":
    main()
