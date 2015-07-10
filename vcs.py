#!/usr/bin/env python
import optfunc
import shutil
import os
import sys
import errno
def ignore_patterns(root):
    try:
        f = open(root + '/.vcsignore')
        lines = [line.strip() for line in f if line.strip()]
        lines.append('.vcs')
        print lines
        return shutil.ignore_patterns(*lines)
    except Exception, e:
        return None

def get_refs(vcsroot):
    refsdir = os.path.join(vcsroot, 'refs')
    mkdir_p(os.path.join(refsdir))
    return sorted(map(int, [os.path.basename(d) for d in os.listdir(refsdir)]))

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def checkout(root, ref):
    try:
        os.listdir(os.path.join(root, '.vcs', 'refs', str(ref)))
    except Exception, e:
        raise Exception('Cannot checkout ref', ref, e)

def commit(root, ref):
    dest = os.path.join(root, '.vcs', 'refs', str(ref))
    try:
        ignore_patterns(root)
        shutil.copytree(root, dest, ignore=ignore_patterns(root))
    except Exception, e:
        raise Exception('Commit error', ref, e)


def main(command, ref=None, root='.'):
    os.chdir = root
    vcsroot = root + '/.vcs'
    refs = get_refs(vcsroot)
    lastref = refs[-1] if refs else 0

    if command == 'checkout':
        if ref == 'latest':
            ref = lastref
        checkout(root, ref)
    elif command == 'commit':
        commit(root, lastref + 1)


if __name__ == '__main__':
    optfunc.run(main)
