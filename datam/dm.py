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
        else:
            self.manifest = []
            self.meta = {}

    def __contains__(self, tag):
        """ """
        for item in self.manifest:
            if item['path'] == tag:
                return True

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

    def validate(self, clone=True):
        """ """
        if not self.manifest:
            logging.debug("manifest is empty!")
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
            print item['path']

def main():
    """ """
    parser = argparse.ArgumentParser(description="datam: data manager")
    parser.add_argument("--manifest", metavar='path', default="manifest.json", help="manifest file")
    parser.add_argument("--add", metavar='path', nargs='*', type=str, help="path to data file")
    parser.add_argument("--pop", metavar='path', nargs='*', type=str, help="remove paths from manifest")
    parser.add_argument("--clone", action='store_true', help="download data files from remote")
    parser.add_argument("--show", action='store_true', help="show contents of manifest file")    
    parser.add_argument("--hash", metavar='path', nargs='*', help="compute hash")
    parser.add_argument("-v", metavar='n', default=1, type=int, help='verbosity')
    args = parser.parse_args()

    if args.v > 0:
        logging.basicConfig(level=logging.DEBUG)

    D = DataManager(path=args.manifest)

    change_flag = False

    if args.hash:
        for path in args.hash:
            print path, compute_hash(path)

    if args.clone:
        D.clone()
        change_flag = True

    if args.add:
        for path in args.add:
            try:
                D.add(path)
                change_flag = True
            except DuplicateFile as message:
                logging.warning(message)

    if args.pop:
        for path in args.pop:
            try:
                D.pop(path)
                change_flag = True
            except DuplicateFile as message:
                logging.warning(message)

    if args.show:
        D.show()

    if change_flag:
        D.write_manifest()

    D.validate()


class DuplicateFile(Exception):
    pass

class DownloadError(Exception):
    pass
