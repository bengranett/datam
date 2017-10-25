""" """
import sys
import os
import logging
import argparse
import json
from pyblake2 import blake2b

import datam

def normpath(path):
    """ Normalize path """
    return os.path.relpath(os.path.realpath(path))


def compute_hash(filename, chunk_size=1048576):
    """ Compute the hash of the file."""
    hasher = blake2b()
    with open(filename, 'rb') as fp:
        while hasher.update(fp.read(chunk_size)):
            pass
    digest = hasher.hexdigest()
    return digest


def clone(remote, local):
    """ Clone the remote file to local directory """
    try:
        os.makedirs(os.path.dirname(local))
    except OSError:
        pass

    logging.debug("Cloning '%s' -> '%s'", remote, local)

    if remote.startswith("http"):
        cmd = "wget -v -O{local} {remote}"
    else:
        cmd = "rsync -v {remote} {local}"

    cmd = cmd.format(remote=remote, local=local)

    logging.debug(cmd)

    res = os.system(cmd)
    if res:
        raise DownloadError("command returned error code: %s"%str(res))


class DataManager(object):
    """ """

    def __init__(self, path="manifest.json"):
        """ """
        self.manifest_path = path
        if os.path.exists(path):
            with open(path) as fp:
                data = json.load(fp)
                self.manifest = data['files']
                self.meta = data['meta']
            logging.debug("loaded manifest '%s'"%path)
        else:
            logging.debug("manifest file not found '%s'"%path)
            self.manifest = []
            self.meta = {}

    def __contains__(self, tag):
        """ """
        for item in self.manifest:
            if item['path'] == tag:
                return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        """ """
        self.write_manifest()

    def write_manifest(self, indent=2):
        """ """
        if not self.manifest:
            return

        self.meta['version'] = datam.__version__
        self.meta['comment'] = "this file was written by {prog} v{version}.".format(prog=sys.argv[0], version=datam.__version__)

        self.manifest.sort(key=lambda x: x["path"])

        out = {
            "meta": self.meta,
            "files": self.manifest
        }

        with open(self.manifest_path,'w') as fp:
            json.dump(out, fp, indent=indent, sort_keys=True)
        logging.debug("wrote '%s'", self.manifest_path)

    def verify(self, clone=True):
        """ """
        if not self.manifest:
            return 

        error_flag = False
        missing_files = []
        wrong_hash = []

        for item in self.manifest:
            path = item['path']

            if not os.path.exists(path):
                error_flag = True
                logging.warning("Missing file: '%s'", path)
                missing_files.append(path)
                continue

            digest = compute_hash(item["path"])

            if not digest == item['digest']:
                error_flag = True
                logging.warning("Wrong hash: '%s'", path)
                wrong_hash.append(path)

        if missing_files:
            logging.warning("There are files missing.  Try running with --clone")

        if wrong_hash:
            logging.warning("Some files have wrong hashes.")

        if not error_flag:
            logging.debug("Looks good! ('%s')", self.manifest_path)

    def clone(self):
        """ """
        for item in self.manifest:
            if os.path.exists(item["path"]):
                continue
            if item.has_key("remote"):
                clone(item["remote"], item["path"])

    def add(self, path, **kwargs):
        """ """
        path = normpath(path)

        if path in self:
            raise DuplicateFile("Path '%s' is already in '%s'."%(path, self.manifest_path))
        digest = compute_hash(path)

        data = {
            'path': path,
            'remote': '',
            'digest': digest,
            'size': os.path.getsize(path),
        }
        data.update(kwargs)
        self.manifest.append(data)
        logging.debug("checked in '%s'", path)

    def pop(self, path):
        """ """
        path = path.strip()
        for i, item in enumerate(self.manifest):
            if item['path'] == path:
                pop = self.manifest.pop(i)
                logging.debug("- %s", pop['path'])
                return

    def show(self):
        if not self.manifest:
            logging.debug("manifest is empty!")
            return 
        for item in self.manifest:
            print "{digest:8.8} {path}".format(**item)


def _add(args):
    with DataManager(path=args.manifest) as D:
        for path in args.path:
            try:
                D.add(path)
            except DuplicateFile as message:
                logging.warning(message)

def _pop(args):
    with DataManager(path=args.manifest) as D:
        for path in args.path:
            D.pop(path)

def _clone(args):
    with DataManager(path=args.manifest) as D:
        D.clone()

def _verify(args):
    with DataManager(path=args.manifest) as D:
        D.clone()

def _show(args):
    with DataManager(path=args.manifest) as D:
        D.show()

def _hash(args):
    for path in args.path:
        print path, compute_hash(path)


def main():
    """ """
    parser = argparse.ArgumentParser(description="datam: data manager")

    parser.add_argument("-m", "--manifest", metavar='path', default="manifest.json", help="manifest file")
    parser.add_argument("-v", "--verbose", metavar='n', default=1, type=int, help='verbosity (0,1,2,3)')

    subparser = parser.add_subparsers(title='commands')

    parser_add = subparser.add_parser('add', help='check in files to manifest')
    parser_add.add_argument("path", metavar='path', nargs='*', type=str, help="path to data file")
    parser_add.set_defaults(func=_add)

    parser_pop = subparser.add_parser('pop', help='remove files from manifest')
    parser_pop.add_argument("path", metavar='path', nargs='*', type=str, help="path to data file")
    parser_pop.set_defaults(func=_pop)

    parser_verify = subparser.add_parser('verify', help='verify local files against manifest')
    parser_verify.set_defaults(func=_verify)

    parser_clone = subparser.add_parser('clone', help='download data files from remote')
    parser_clone.set_defaults(func=_clone)

    parser_show = subparser.add_parser('show', help='show contents of manifest file')
    parser_show.set_defaults(func=_show)

    parser_hash = subparser.add_parser('hash', help='compute hash of file and print to screen')
    parser_hash.add_argument("path", metavar='path', nargs='*', type=str, help="path to data file")
    parser_hash.set_defaults(func=_hash)

    args = parser.parse_args()

    if args.verbose > 2:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose > 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    args.func(args)


class DuplicateFile(Exception):
    pass

class DownloadError(Exception):
    pass
