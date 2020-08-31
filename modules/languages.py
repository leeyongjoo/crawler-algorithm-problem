extensions = {
    'python': '.py',
    'c': '.c',
    'c++': '.cpp',
    'java': '.java',
}


def get_languages():
    return list(extensions.keys())


def get_extension(language):
    return extensions[language]
