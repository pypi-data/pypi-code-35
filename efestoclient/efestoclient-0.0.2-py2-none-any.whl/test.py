from __init__ import EfestoClient

test = EfestoClient('https://evastampaggi.efesto.web2app.it', 'kenneth.blieck@gmail.com', 'E12b03k17', '886B0F8B53F4')
print test.get_status()