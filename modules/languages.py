extensions = {
    'json': '.json',
    'python': '.py',
    'c': '.c',
    'c++': '.cpp',
    'java': '.java',
}


def get_languages():
    return list(extensions.keys())[1:]


def get_extension(language):
    return extensions[language]
