from lxml import etree
import argparse
import os
import errno

def ensure_path(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

parser = argparse.ArgumentParser()
parser.add_argument('source_file', help = 'Full path of the source .tmx file')
args = parser.parse_args()
if not os.path.isfile(args.source_file):
    print 'Error! Source file specified doesn\'t exist.'
    exit()

file_name = args.source_file
if '/' in args.source_file:
    file_name = args.source_file[args.source_file.rfind('/')+1:-4]
#    print file_name

ensure_path("./converted_files")
wfile = open('./converted_files/{filename}_converted.tmx'.format(filename=file_name),'w')

wfile.write('<?xml version="1.0" encoding="utf-8"?>\n')
initialContext = etree.iterparse(args.source_file,events=('start',))
for event, begintags in initialContext:
    if begintags.tag == 'body':
        begintags.clear()
        break
    elif begintags.tag == 'header':
        wfile.write(etree.tostring(begintags, encoding='utf-8', pretty_print=True))
        begintags.clear()
    elif begintags.tag == 'tmx':
#        print begintags.attrib
        wfile.write('<tmx')
        for name, value in begintags.items():
            wfile.write(' {pname}="{pvalue}"'.format(pname=name,pvalue=value))
        wfile.write('>\n')

wfile.write('<body>\n')

context = etree.iterparse(args.source_file, events=('end',), tag='tu')
for event, tus in context:
    tus.attrib.clear()
    seg_text_src = tus.xpath('./tuv[@xml:lang="en"]/seg/text()')
#    print seg_text_src
    seg_text_target = tus.xpath('./tuv[@xml:lang="hi"]/seg/text()')
#    print seg_text_target
    segs = tus.xpath('.//seg')
    text_count = 0
    for seg in segs:
        for children in seg:
            children.getparent().remove(children)
        if text_count == 0:
            seg.text = ' '.join(seg_text_src)
        else:
            seg.text = ' '.join(seg_text_target)
        text_count += 1
        props = seg.xpath('preceding-sibling::*')
        for prop in props:
            tus.insert(0, prop)
    wfile.write(etree.tostring(tus,encoding='utf-8',pretty_print=True))
    tus.clear()
wfile.write('</body>\n</tmx>')
wfile.close()
print 'File successfully converted.'
