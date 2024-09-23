# utils.py
import os

def get_file_names(blobName):
    file_name = os.path.basename(blobName)
    file_root, file_extension = os.path.splitext(file_name)
    return file_name, file_root

def get_words(page, line):
    result = []
    for word in page.words:
        if _in_span(word, line.spans):
            result.append(word)
    return result

def _in_span(word, spans):
    for span in spans:
        if word.span.offset >= span.offset and (word.span.offset + word.span.length) <= (span.offset + span.length):
            return True
    return False