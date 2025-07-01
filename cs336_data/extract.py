from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse import detect_encoding
from resiliparse.extract.html2text import extract_plain_text
def extract_text(data: bytes):
    format = detect_encoding(data)
    string = data.decode(encoding=format)
    return extract_plain_text(string)