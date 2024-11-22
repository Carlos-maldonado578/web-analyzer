def detect_blog(links):
    for link in links:
        if 'blog' in link.lower():
            return link
    return None
