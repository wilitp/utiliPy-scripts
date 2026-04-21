"""
turns a source pdf into a booklet suitable for bookbinding.

you can adjust signature sizes.
"""


import PyPDF2
import re, sys


signature = None
starting_offset = 0
ending_offset = 0

assert len(sys.argv) >= 4

in_fpath= sys.argv[1]
in_stream = open(in_fpath)

out_fpath = sys.argv[2]
out_stream = open(out_fpath, "wb")

try:
    signature = int(sys.argv[3])
except ValueError as e:
    print("Invalid signature argument")
    exit(1)

if len(sys.argv) >= 5:
    try:
        starting_offset = int(sys.argv[4])
    except ValueError as e:
        print("Invalid starting_offset argument")
        exit(1)
if len(sys.argv) >= 6:
    try:
        ending_offset = int(sys.argv[5])
    except ValueError as e:
        print("Invalid ending_offset argument")
        exit(1)

    

signature = signature or 16

assert signature % 4 == 0

def print_usage():
    print("You used this wrong! usage: TODO")

if None in [in_fpath, out_fpath, signature]:
    print_usage()
    
    exit(1)
        


# Initialize PDF reader & writer objects
in_file = PyPDF2.PdfReader(in_fpath) 

# file used for padding only
aux_file = PyPDF2.PdfWriter()

if missing_pages := len(in_file.pages) % signature != 0:
    for page in in_file.pages:
        aux_file.add_page(page)
    for _ in range(missing_pages):
        aux_file.add_blank_page()

    in_file = aux_file

out_file = PyPDF2.PdfWriter()


def order_signature(pages_to_order: list[PyPDF2.PageObject], signature_size: int) -> list[PyPDF2.PageObject]:
    if len(pages_to_order) != signature_size:
        return pages_to_order
    else:
        ret = []
        for i in range(signature_size // 2):
            if i % 2 == 0:
                ret.extend([pages_to_order[-(i + 1)], pages_to_order[i]])
            else:
                ret.extend([pages_to_order[i], pages_to_order[-(i + 1)]])

        return ret



def order_as_booklet(
    in_file: PyPDF2.PdfReader | PyPDF2.PdfWriter, 
    out_file: PyPDF2.PdfWriter, 
    signature_size: int
):
    for sig_index in range(len(in_file.pages) // signature_size + 1):
        # get pages for current signature
        pages_to_order = list(in_file.pages[sig_index * signature_size : min((sig_index + 1) * signature_size, len(in_file.pages))])

        # order the signature as booklet and output to new file
        for p in order_signature(pages_to_order, signature_size):
            out_file.add_page(p)



order_as_booklet(in_file, out_file, signature)


out_file.write(out_stream)
