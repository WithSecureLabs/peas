__author__ = 'Adam Rutherford'

import sys
import os
import hashlib
import errno
from random import choice
from string import ascii_uppercase, digits
from optparse import OptionParser

import peas
from pathlib import Path, PureWindowsPath

R = '\033[1;31m'  # RED
G = '\033[0;32m'  # GREEN
Y = '\033[0;33m'  # YELLOW
M = '\033[0;35m'  # MAGENTA
S = '\033[0m'     # RESET


def info(msg):
    sys.stdout.write('{0}[*] {1}{2}\n'.format(G, msg, S))


def warning(msg):
    sys.stdout.write('{0}[!] {1}{2}\n'.format(Y, msg, S))


def error(msg):
    sys.stderr.write('{0}[-] {1}{2}\n'.format(R, msg, S))


def positive(msg):
    sys.stdout.write('{0}[+] {1}{2}\n'.format(G, msg, S))


def split_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


def create_arg_parser():

    usage = "python -m peas [options] <server>"
    parser = OptionParser(usage=usage)

    # Settings:
    parser.add_option("-u", None, dest="user",
                      help="username", metavar="USER")

    parser.add_option("-p", None, dest="password",
                      help="password", metavar="PASSWORD")

    parser.add_option("-q", None, dest="quiet",
                      action="store_true", default=False,
                      help="suppress all unnecessary output")

    parser.add_option("--smb-user", None,
                      dest="smb_user",
                      help="username to use for SMB operations",
                      metavar="USER")

    parser.add_option("--smb-pass", None,
                      dest="smb_password",
                      help="password to use for SMB operations",
                      metavar="PASSWORD")

    parser.add_option("--verify-ssl", None, dest="verify_ssl",
                      action="store_true", default=False,
                      help="verify SSL certificates (important)")

    parser.add_option("-o", None, dest="file",
                      help="output to file", metavar="FILENAME")

    parser.add_option("-O", None, dest="output_dir",
                      help="output directory (for specific commands only, not combined with -o)", metavar="PATH")

    parser.add_option("-F", None, dest="format",
                      help="output formatting and encoding options",
                      metavar="repr,hex,b64,stdout,stderr,file")

    parser.add_option("--pattern", None, type="string", dest="pattern",
                      action="callback", callback=split_args,
                      help="filter files by comma-separated patterns (--crawl-unc)")

    parser.add_option("--download", None, dest="download",
                      action="store_true", default=False,
                      help="download files at a given UNC path while crawling (--crawl-unc)")

    parser.add_option("--prefix", None, dest="prefix",
                      help="NetBIOS hostname prefix (--brute-unc)")

    # Functionality:
    parser.add_option("--check", None,
                      action="store_true", dest="check",
                      help="check if account can be accessed with given password")

    parser.add_option("--emails", None,
                      action="store_true", dest="extract_emails",
                      help="retrieve emails")

    parser.add_option("--list-unc", None,
                      dest="list_unc",
                      help="list the files at a given UNC path",
                      metavar="UNC_PATH")

    parser.add_option("--dl-unc", None,
                      dest="dl_unc",
                      help="download the file at a given UNC path",
                      metavar="UNC_PATH")

    parser.add_option("--crawl-unc", None,
                      dest="crawl_unc",
                      help="recursively list all files at a given UNC path",
                      metavar="UNC_PATH")

    parser.add_option("--brute-unc", None,
                      action="store_true", dest="brute_unc",
                      help="recursively list all files at a given UNC path")

    return parser


def init_authed_client(options, verify=True):

    if options.user is None:
        error("A username must be specified for this command.")
        return False
    if options.password is None:
        error("A password must be specified for this command.")
        return False

    client = peas.Peas()

    creds = {
        'server': options.server,
        'user': options.user,
        'password': options.password,
    }
    if options.smb_user is not None:
        creds['smb_user'] = options.smb_user
    if options.smb_password is not None:
        creds['smb_password'] = options.smb_password

    client.set_creds(creds)

    if not verify:
        client.disable_certificate_verification()

    return client


def check_server(options):

    client = peas.Peas()

    client.set_creds({'server': options.server})

    if not options.verify_ssl:
        client.disable_certificate_verification()

    result = client.get_server_headers()
    output_result(str(result), options, default='stdout')


def check(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    creds_valid = client.check_auth()
    if creds_valid:
        positive("Auth success.")
    else:
        error("Auth failure.")


def extract_emails(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    emails = client.extract_emails()
    # TODO: Output the emails in a more useful format.
    for i, email in enumerate(emails):

        if options.output_dir:
            fname = 'email_%d_%s.xml' % (i, hashlib.md5(email).hexdigest())
            path = os.path.join(options.output_dir, fname)
            open(path, 'wb').write(email.strip() + '\n')
        else:
            output_result(email + '\n', options, default='repr')

    if options.output_dir:
        info("Wrote %d emails to %r" % (len(emails), options.output_dir))


def list_unc_helper(client, uncpath, options, show_parent=True):

    records = client.get_unc_listing(uncpath)

    output = []

    if not options.quiet and show_parent:
        info("Listing: %s\n" % (uncpath,))

    for record in records:

        name = record.get('DisplayName')
        uncpath = record.get('LinkId')
        is_folder = record.get('IsFolder') == '1'
        is_hidden = record.get('IsHidden') == '1'
        size = record.get('ContentLength', '0') + 'B'
        ctype = record.get('ContentType', '-')
        last_mod = record.get('LastModifiedDate', '-')
        created = record.get('CreationDate', '-')

        attrs = ('f' if is_folder else '-') + ('h' if is_hidden else '-')

        output.append("%s %-24s %-24s %-24s %-12s %s" % (attrs, created, last_mod, ctype, size, uncpath))

    output_result('\n'.join(output), options, default='stdout')


def list_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    list_unc_helper(client, options.list_unc, options)


def dl_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    path = options.dl_unc
    data = client.get_unc_file(path)

    if not options.quiet:
        info("Downloading: %s\n" % (path,))

    output_result(data, options, default='repr')


def crawl_unc_helper(client, uncpath, patterns, options):

    records = client.get_unc_listing(uncpath)
    for record in records:
        if record['IsFolder'] == '1':
            if record['LinkId'] == uncpath:
                continue
            crawl_unc_helper(client, record['LinkId'], patterns, options)
        else:
            for pattern in patterns:
                if pattern.lower() in record['LinkId'].lower():
                    if options.download:
                        try:
                            data = client.get_unc_file(record['LinkId'])
                        except TypeError:
                            pass
                        else:
                            winpath = PureWindowsPath(record['LinkId'])
                            posixpath = Path(winpath.as_posix()) # Windows path to POSIX path
                            posixpath = Path(*posixpath.parts[1:]) # get rid of leading "/"
                            dirpath = posixpath.parent
                            newdirpath = mkdir_p(dirpath)
                            filename = str(newdirpath / posixpath.name)
                            try:
                                with open(filename, 'w') as fd:
                                    fd.write(data)
                            # If path name becomes too long when filename is added
                            except IOError as e:
                                if e.errno == errno.ENAMETOOLONG:
                                    rootpath = Path(newdirpath.parts[0])
                                    extname = posixpath.suffix
                                    # Generate random name for the file and put it in the root share directory
                                    filename = ''.join(choice(ascii_uppercase + digits) for _ in range(8)) + extname
                                    filename = str(rootpath / filename)
                                    with open(filename, 'w') as fd:
                                        fd.write(data)
                                    warning('File %s"%s"%s was renamed and written to %s"%s"%s' % (M, str(posixpath), S, M, filename, S))
                                else:
                                    raise
                            else:
                                if dirpath != newdirpath:
                                    warning('File %s"%s"%s was written to %s"%s"%s' % (M, str(posixpath), S, M, filename, S))
                    else:
                        list_unc_helper(client, record['LinkId'], options, show_parent=False)

                    break


def crawl_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    if options.pattern:
        patterns = options.pattern
    else:
        patterns = ['']

    if options.download:
        info('Listing and downloading all files: %s\n' % (options.crawl_unc))
    else:
        info('Listing all files: %s\n' % (options.crawl_unc))

    crawl_unc_helper(client, options.crawl_unc, patterns, options)


def generate_wordlist(prefix=None):

    hostnames = [
        'DC', 'WEB', 'DEV', 'SQL', 'RDS',
        'TS', 'TER', 'TERM', 'JIRA', 'FS',
        'EXCH', 'EX', 'CRM', '1C', 'WIN',
        'NAP', 'SKUD', 'SEC', 'WSUS', 'PC',
        'WS', 'MN'
    ]

    wordlist = []
    if prefix is not None:
        for h in hostnames:
            for i in range(1, 5):
                wordlist.append('{prefix}{i:02}-{h}'.format(prefix=prefix, i=i, h=h))  # PREFIX01-DC
                wordlist.append('{prefix}{i}-{h}'.format(prefix=prefix, i=i, h=h))     # PREFIX1-DC
                for j in range(1, 10):
                    wordlist.append('{prefix}{i:02}-{h}-{j:02}'.format(prefix=prefix, i=i, h=h, j=j))  # PREFIX01-DC-01
                    wordlist.append('{prefix}{i}-{h}-{j:02}'.format(prefix=prefix, i=i, h=h, j=j))     # PREFIX1-DC-01
                    wordlist.append('{prefix}{i:02}-{h}-{j}'.format(prefix=prefix, i=i, h=h, j=j))     # PREFIX01-DC-1
                    wordlist.append('{prefix}{i}-{h}-{j}'.format(prefix=prefix, i=i, h=h, j=j))        # PREFIX1-DC-1
                    wordlist.append('{prefix}{i:02}-{h}{j:02}'.format(prefix=prefix, i=i, h=h, j=j))   # PREFIX01-DC01
                    wordlist.append('{prefix}{i}-{h}{j:02}'.format(prefix=prefix, i=i, h=h, j=j))      # PREFIX1-DC01
                    wordlist.append('{prefix}{i:02}-{h}{j}'.format(prefix=prefix, i=i, h=h, j=j))      # PREFIX01-DC1
                    wordlist.append('{prefix}{i}-{h}{j}'.format(prefix=prefix, i=i, h=h, j=j))         # PREFIX1-DC1

    for h in hostnames:
        wordlist.append(h)  # DC
        for i in range(1, 10):
            wordlist.append('{h}-{i:02}'.format(h=h, i=i))  # DC-01
            wordlist.append('{h}-{i}'.format(h=h, i=i))     # DC-1
            wordlist.append('{h}{i:02}'.format(h=h, i=i))   # DC01
            wordlist.append('{h}{i}'.format(h=h, i=i))      # DC1

    return wordlist


def brute_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    wordlist = generate_wordlist(options.prefix.upper())
    for w in wordlist:
        list_unc_helper(client, r'\\%s' % w, options, show_parent=False)


def output_result(data, options, default='repr'):

    fmt = options.format
    if not fmt:
        fmt = 'file' if options.file else default
    actions = fmt.split(',')

    # Write to file at the end if a filename is specified.
    if options.file and 'file' not in actions:
        actions.append('file')

    # Process the output based on the format/encoding options chosen.
    encoding_used = True
    for action in actions:
        if action == 'repr':
            data = repr(data)
            encoding_used = False
        elif action == 'hex':
            data = data.encode('hex')
            encoding_used = False
        elif action in ['base64', 'b64']:
            data = data.encode('base64')
            encoding_used = False
        elif action == 'stdout':
            print(data)
            encoding_used = True
        elif action == 'stderr':
            sys.stderr.write(data)
            encoding_used = True
        # Allow the user to write the file after other encodings have been applied.
        elif action == 'file':
            if options.file:
                open(options.file, 'wb').write(data)
                if not options.quiet:
                    info("Wrote %d bytes to %r." % (len(data), options.file))
            else:
                error("No filename specified.")
            encoding_used = True

    # Print now if an encoding has been used but never output.
    if not encoding_used:
        print(data)


def process_options(options):

    # Create the output directory if necessary.
    if options.output_dir:
        try:
            os.makedirs(options.output_dir)
        except OSError:
            pass

    return options


def mkdir_p(dirpath):

    try:
        dirname = str(dirpath)
        os.makedirs(dirname)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        # If directory path name already too long
        elif e.errno == errno.ENAMETOOLONG:
            dirpath = Path(dirpath.parts[0])
        else:
            raise

    return dirpath


def main():

    # Parse the arguments to the program into an options object.
    arg_parser = create_arg_parser()
    (options, args) = arg_parser.parse_args()

    if not options.quiet:
        peas.show_banner()

    options = process_options(options)

    # The server is required as an argument.
    if not args:
        arg_parser.print_help()
        return
    options.server = args[0]

    # Perform the requested functionality.
    ran = False
    if options.check:
        check(options)
        ran = True
    if options.extract_emails:
        extract_emails(options)
        ran = True
    if options.list_unc:
        list_unc(options)
        ran = True
    if options.dl_unc:
        dl_unc(options)
        ran = True
    if options.crawl_unc:
        crawl_unc(options)
        ran = True
    if options.brute_unc:
        brute_unc(options)
        ran = True
    if not ran:
        check_server(options)


if __name__ == '__main__':
    main()
