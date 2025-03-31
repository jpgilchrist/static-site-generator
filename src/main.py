import shutil
import sys

from utils import generate_all, copy_all

CONTENT_DIR = "content"
STATIC_DIR = "static"
OUTPUT_DIR = "docs"

def build(base_path = "/"):
    print("Building docs...", base_path)
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    copy_all(STATIC_DIR, OUTPUT_DIR)
    generate_all(CONTENT_DIR, OUTPUT_DIR, base_path=base_path)


def main():
    if len(sys.argv) > 1:
        build(sys.argv[1])
    else:
        build()


if __name__ == "__main__":
    main()
