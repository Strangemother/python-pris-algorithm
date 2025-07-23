from collections import defaultdict
from inspect import isfunction


def bool_pr(key, items, true='+'):
    # return ['', true][key in items]
    return str_bool(key in items, true)


def str_bool(val, true='+'):
    return ['', true][val]



def print_table(lines, ml):
    for l in lines:
        if l is None:
            print('')
            continue

        pr(f"  {l[0]:<{ml}} {l[1]:^4} | {l[2]:^6} | {l[3]:^4} | {l[4]:^4} | {l[5]:^4} | {l[6]:^4}")


def pr(*a):
    print(' '.join(a))



class PrintTableMixin(object):

    def print_state_table(self, hots=None, matches=None, drops=None):
        """print a table of the current state, inject hots, matches or drops
        to highlight within the table.

            self.print_state_table('ape',('ww', 'echo','w', ), 'yeswno' )

        """
        hots = hots or ()
        matches = matches or ()
        drops = drops or ()

        return self.print_insert_table(None, hots, matches, drops)

    def print_insert_table(self, char, _hots, matches, drops, header=True):
        opens = ()
        lines = ()
        ml = 4
        spacer = None
        if header is True:
            _header = ('WORD', 'POS', 'NEXT', 'STRT', 'OPEN', 'HIT', 'DROP', )
            lines += ( spacer, _header, )
        for tk, v in self.table.items():
            stk = str(tk)
            # if v < 0:
            #     continue
            ml = max(ml, len(stk)+1)
            opens += ( (stk,v,), )
            _next = '' # stk[0]
            if v > -1:
                try:
                    # _next = stk[v]# if v > -1 else 0]
                    f = self.get_sequence(stk)[v]
                    if isfunction(f):
                        f = 'f()'
                    _next = str(f)
                except IndexError:
                    pass

            line = (
                    stk,
                    v if v > -1 else '',
                    _next,
                    bool_pr(stk, _hots, '#'),# 'started'),
                    str_bool(v > -1, '#'),# 'open'),
                    bool_pr(stk, matches, '#'),# 'match'),
                    bool_pr(stk, drops, '#'),# 'dropped'),
                )

            lines += ( line, )

        # print(k, sequences.table, )
        # print(', '.join(_hots), ' | ',
        #     ', '.join(matches), ' | ',
        #     ', '.join(drops))
        print_table(lines, ml)


    def table_insert_keys(self, chars):
        res = None
        for k in chars:
            res = self.insert_keys(k) # _hots, matches, drops
            # self.print_insert_table(k, *res)
        return res

