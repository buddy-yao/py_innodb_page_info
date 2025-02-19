# encoding=utf-8
import os
from include import *

TABLESPACE_NAME = 'D:\\mysql_data\\test\\t.ibd'
VARIABLE_FIELD_COUNT = 1
NULL_FIELD_COUNT = 0


class myargv(object):
    def __init__(self, argv):
        self.argv = argv
        self.parms = {}
        self.tablespace = ''

    def parse_cmdline(self):
        argv = self.argv
        if len(argv) == 1:
            print('Usage: python py_innodb_page_info.py [OPTIONS] tablespace_file')
            print('For more options, use python py_innodb_page_info.py -h')
            return 0
        while argv:
            if argv[0][0] == '-':
                if argv[0][1] == 'h':
                    self.parms[argv[0]] = ''
                    argv = argv[1:]
                    break
                if argv[0][1] == 'v':
                    self.parms[argv[0]] = ''
                    argv = argv[1:]
                else:
                    self.parms[argv[0]] = argv[1]
                    argv = argv[2:]
            else:
                self.tablespace = argv[0]
                argv = argv[1:]
        if '-h' in self.parms:
            print('Get InnoDB Page Info')
            print('Usage: python py_innodb_page_info.py [OPTIONS] tablespace_file\n')
            print('The following options may be given as the first argument:')
            print('-h        help ')
            print('-o output put the result to file')
            print('-t number thread to anayle the tablespace file')
            print('-v        verbose mode')
            return 0
        return 1


def mach_read_from_n(page, start_offset, length):
    return page[start_offset:start_offset + length].hex()


def get_innodb_page_type(myargv):
    f = open(myargv.tablespace, 'rb')
    fsize = int(os.path.getsize(f.name) / INNODB_PAGE_SIZE)
    ret = {}
    for i in range(fsize):
        page = f.read(INNODB_PAGE_SIZE)
        page_offset = mach_read_from_n(page, FIL_PAGE_OFFSET, 4)
        page_type = mach_read_from_n(page, FIL_PAGE_TYPE, 2)
        if '-v' in myargv.parms:
            if page_type == '45bf':
                page_level = mach_read_from_n(page, FIL_PAGE_DATA + PAGE_LEVEL, 2)
                index_id = mach_read_from_n(page, FIL_PAGE_DATA + PAGE_LEVEL+2, 8)
                print("page offset %d, page type <%s>, page level <%d>, index id <%d>" % (
                    int(page_offset, 16), innodb_page_type[page_type], int(page_level, 16), int(index_id, 16)))
            else:
                print("page offset %s, page type <%s>" % (int(page_offset, 16), innodb_page_type[page_type]))
        if page_type not in ret:
            ret[page_type] = 1
        else:
            ret[page_type] = ret[page_type] + 1
    print("Total number of page: %d:" % fsize)
    for typ in ret:
        print("%s: %s" % (innodb_page_type[typ], ret[typ]))
