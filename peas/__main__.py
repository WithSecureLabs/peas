__author__ = 'Adam Rutherford'

import sys
import os
import hashlib
from optparse import OptionParser

import peas


def error(msg):
    sys.stderr.write("[-] " + msg + "\n")


def positive(msg):
    sys.stdout.write("[+] " + msg + "\n")


def negative(msg):
    sys.stdout.write("[-] " + msg + "\n")


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
        negative("Auth failure.")


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
        print("Wrote %d emails to %r" % (len(emails), options.output_dir))


def list_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    path = options.list_unc
    records = client.get_unc_listing(path)

    output = []

    if not options.quiet:
        print("Listing: %s\n" % (path,))

    for record in records:

        name = record.get('DisplayName')
        path = record.get('LinkId')
        is_folder = record.get('IsFolder') == '1'
        is_hidden = record.get('IsHidden') == '1'
        size = record.get('ContentLength', '0') + 'B'
        ctype = record.get('ContentType', '-')
        last_mod = record.get('LastModifiedDate', '-')
        created = record.get('CreationDate', '-')

        attrs = ('f' if is_folder else '-') + ('h' if is_hidden else '-')

        output.append("%s %-24s %-24s %-24s %-12s %s" % (attrs, created, last_mod, ctype, size, path))

    output_result('\n'.join(output) + '\n', options, default='stdout')


def dl_unc(options):

    client = init_authed_client(options, verify=options.verify_ssl)
    if not client:
        return

    path = options.dl_unc
    data = client.get_unc_file(path)

    if not options.quiet:
        print("Downloading: %s\n" % (path,))

    output_result(data, options, default='repr')


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
                    print("Wrote %d bytes to %r." % (len(data), options.file))
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
    if not ran:
        check_server(options)


if __name__ == '__main__':
    main()
