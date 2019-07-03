import lxml.etree as E
import textwrap
import logging
import os

PREFIXES = {
    'b': '**',
    'em': '*',
    's': '~~',
    'h1': '# ',
    'h2': '## ',
    'h3': '### ',
    'h4': '#### ',
    'h5': '##### ',
    'h6': '###### ',
    'p': '    '
}

POSTFIXES = {
    'b': '**',
    'em': '*',
    's': '~~',
    'br': '\n',
}

DOMAIN = 'invisibleup.com'
PORT = '70'

def fix_path(basepath, path):
    if path.startswith(basepath):
        path = os.path.normpath(path)
    else:
        path = os.path.normpath(basepath + path)
    path = path.replace('\\', '/')
    if path[0] == '/':
        path = path[1:]
    if '.' not in path and path[-1] != '/':
        path += '/'
    return path

def img_tag(tag, basepath):
    ''' Handler for <img> tags '''
    path = tag.get('src')
    alt = tag.get('alt')
    if path is None:
        return ''
    if alt is None:
        alt = os.path.basename(path)
    if 'http' in path:
        # External HTTP link
        return f'{alt}\tURL:{path}\t{DOMAIN}\t{PORT}\n'
    else:
        # Local Image
        path = fix_path(basepath, path)
        return f'I{alt}\t{path}\t{DOMAIN}\t{PORT}\n'

def a_tag(tag, basepath):
    ''' Handler for <a> tags '''
    # this is complicated
    if not tag.get('href'):
        return ''

    path = tag.get('href')
    if 'http' in path:
        # External HTTP link
        return f'h{tag.text}\tURL:{path}\t{DOMAIN}\t{PORT}\n'
    elif 'gopher://' in path:
        # External Gopher link
        splitted = path.split('/')
        try:
            domain, port = splitted[2].split(':')
        except ValueError:
            domain = splitted[2]
            port = '70'
        path = '/'.join(splitted[3:])
        return f'1{tag.text}\t{path}\t{domain}\t{port}\n'
    elif '.png' in path or '.jpg' in path or '.gif' in path:
        # Image
        path = fix_path(basepath, path)
        return f'I{tag.text}\t{path}\t{DOMAIN}\t{PORT}\n'
    elif '.ips' in path or '.zip' in path or '.exe' in path:
        # Some sort of binary something or other
        path = fix_path(basepath, path)
        return f'9{tag.text}\t{path}\t{DOMAIN}\t{PORT}\n'
    else:
        # Likely an internal Gopherspace link
        path = fix_path(basepath, path)
        return f'1{tag.text}\t{path}\t{DOMAIN}\t{PORT}\n'
    # TODO: External gopherspace links

def html2gopher(tag, basepath, width=80):
    output: str = ''

    if isinstance(tag, E._Comment):
        return ''

    if tag.text is None:
        tag.text = ''
    if tag.tail is None:
        tag.tail = ''

    if tag.tag != 'pre':
        tag.text = tag.text.replace('\n', ' ')
        tag.text = tag.text.replace('\t', '')
        tag.tail = tag.tail.replace('\n', ' ')
        tag.tail = tag.tail.replace('\t', '')

    # Tag prefix
    if tag.tag in PREFIXES:
        tag.text = PREFIXES[tag.tag] + tag.text
    # Postfix
    if tag.tag in POSTFIXES:
        tag.text += POSTFIXES[tag.tag]

    # Add content
    if tag.tag == 'a':
        output = a_tag(tag, basepath)
    elif tag.tag == 'img':
        output = img_tag(tag, basepath)
    elif tag.tag == 'hr':
        output += '-' * width
    elif tag.tag == 'td':
        output += tag.text
        output += '\n' + '-' * width
    elif tag.tag == 'tr':
        output += '\n' + '=' * width
    elif tag.tag == 'th':
        output += tag.text
        output += '\n' + '+=' * (width // 2)
    else:
        output += tag.text

    # Run recursively for each subnode
    for child in tag:
        if child.tag == 'a':
            output += '\n' + html2gopher(child, basepath, width)
        elif tag.tag == 'a' and child.tag == 'img':
            # lol whoops use alt as the label
            tag.text = child.get('alt')
            output = a_tag(tag, basepath)
        elif child.tag == 'style' or child.tag == 'script':
            continue
        elif child.tag == 'form' or (
            child.get('class') is not None and
            'gopherignore' in child.get('class')
        ):
            output += ' ' * 12 + 'Interactive content not available via Gopher\n'
        else:
            output += html2gopher(child, basepath, width)

    # "Tail"
    if tag.tail is not None:
        output += tag.tail

    del tag # being too cautious...

    # Word wrap
    output2 = ''
    for line in output.splitlines():
        if line.count('\t') != 3:
            output2 += '\n'.join(textwrap.wrap(line, width)) + '\n'
        else:
            label, url, host, port = line.split('\t')
            rsctype = label[0]
            label = label[1:]
            labels = textwrap.wrap(label, width)
            del label
            for label in labels:
                output2 += rsctype + label + '\t' + url + '\t' + host + '\t' + port + '\n'

    del output
    return output2
