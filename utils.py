def domain_finder(link):
    import string
    dot_splitter = link.split('.')

    seperator_first = 0
    if '//' in dot_splitter[0]:
        seperator_first = (dot_splitter[0].find('//') + 2)

    seperator_end = ''
    for i in dot_splitter[2]:
        if i in string.punctuation:
            seperator_end = i
            break

    if seperator_end:
        end_ = dot_splitter[2].split(seperator_end)[0]
    else:
        end_ = dot_splitter[2]

    domain = [dot_splitter[0][seperator_first:], dot_splitter[1], end_]
    domain = '.'.join(domain)

    return domain


import os, shutil
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if 'build' not in s:
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

        print("creating new app in " + d)


def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)


def forceCopyFile (sfile, dfile):
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)
