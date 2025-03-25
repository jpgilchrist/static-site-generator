def markdown_to_blocks(markdown):
    if markdown is None:
        return []

    return list(
        filter(lambda x: x != "", map(lambda x: x.strip(), markdown.split("\n\n")))
    )
