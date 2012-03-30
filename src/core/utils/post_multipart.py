# -*- coding: utf-8 -*-

# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
import httplib
import mimetypes

#XXX: это весьма ограниченный конструктор multipart запросов:
# 1) не поддерживаются не ascii имена полей (нужно использовать quopri),
# 2) нельзя управлять content-type полей
# 3) unicode-значения полей считаются text/plain, и передаются в utf-8


def force_str(s, encoding='utf-8'):
    if isinstance(s, unicode):
        return s.encode(encoding)
    return str(s)

#FIXME: не ascii-имена файлов вообще-то требуется кодировать в quoted-printable


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        if isinstance(value, unicode):
            L.append('Content-Type: text/plain; charset=utf-8')
        L.append('')
        L.append(force_str(value))
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

#from email import MIMEText, MIMEImage, MIMEMultipart, MIMENonMultipart
#import email.Encoders
## force email module to disable base64 encoding on bodies in utf-8
#email.Charset.add_charset('utf-8', email.Charset.SHORTEST, None)
#
#def create_upload_post(fields, files, charset='utf-8'):
#    parts = []
#    for (key,value) in fields:
#        part = MIMEText.MIMEText(str(value), 'plain', charset)
#        part.add_header('Content-Disposition', 'form-data', name=key)
#        parts.append(part)
#    for (key, filename, value) in files:
#        try:
#            part = MIMEImage.MIMEImage(value)
#        except TypeError:
#            content_type = get_content_type(filename)
#            part = MIMENonMultipart.MIMENonMultipart(*content_type.split('/'))
#            part.set_payload(value)
#            email.Encoders.encode_base64(part)
#        part.add_header('Content-Disposition', 'form-data', name=key, filename=filename)
#        parts.append(part)
#    m = MIMEMultipart.MIMEMultipart('form-data', None, parts)
#    return m.as_string()


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def post_multipart(host, port, selector, fields, files, headers=None):
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPConnection(host, port)
    all_headers = {
        'Content-Type': content_type
        }
    if headers:
        all_headers.update(headers)
    h.request('POST', selector, body, all_headers)
    res = h.getresponse()
    return res.status, res.reason, res.read()
