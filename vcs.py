#!/usr/bin/env python
import optfunc
import shutil

def ignore_patterns(root):
    try:
        f = open(root + '/.vcsignore')
        lines = [line.strip() for line in f if line.strip()]
        lines.append('.vcs/')
        return shutil.ignore_patterns()
    except Exception, e:
        return None

def main(root):
    dest = root + '/.vcs'
    try:
        shutil.copytree(root, dest, ignore_patterns(root))
    except Exception, e:
        print 'Exception', e


if __name__ == '__main__':
    optfunc.run(main)
