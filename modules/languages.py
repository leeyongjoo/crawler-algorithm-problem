extensions = {
    'python': '.py',
    'c': '.c',
    'c++': '.cpp',
    'java': '.java',
}

language_code = {
    'c': 0,
    'c++': 1,
    'java': 3,
    'python': 6,
}

def get_languages():
    return list(extensions.keys())


def get_extension(language):
    return extensions[language]
