import shutil

from utils import generate_all, copy_all


def build():
    shutil.rmtree("public", ignore_errors=True)
    copy_all("static", "public")
    generate_all("./content", "./public")


def main():
    build()


if __name__ == "__main__":
    main()
