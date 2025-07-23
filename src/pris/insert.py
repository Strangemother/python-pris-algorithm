from inspect import isfunction

class InsertMixin(object):

    def insert_keys(self, *chars):
        """Insert am args iterable of items (chars).

        Return new "hots", "matches", and "drops"
        """
        drops, matches, new_hots = set(), set(), set()

        update = lambda x,y:x.update(set(y))
        as_tuples = lambda *v: tuple(tuple(x) for x in v)

        for c in chars:
            hots, _matches, _drops = self.insert_key(c)
            update(new_hots, hots)
            update(matches, _matches)
            update(drops, _drops)

        return as_tuples(new_hots, matches, drops)

    # def tick_sleeping(self):
    #     """Increment all sleeping positions by 1 until the value reaches -1"""
    #     table = self.table
    #     for table_id, pos in table.items():
    #         if pos >= -1: continue
    #         print('Tick', table_id, pos +1)
    #         table[table_id] = pos + 1

    def insert_key(self, char, reset_on_fail=True):
        matches = ()
        resets = ()
        table = self.table

        _hots = self.set_next_hots(char)
        # self.tick_sleeping()

        for table_id, pos in table.items():
            ## Testing for -1 assumes the hot starts have stepped any active
            # sequence to 0.
            if pos <= -1: continue

            success, res = self._test_insert_key(char, table_id, pos, table)

            if not success:
                if reset_on_fail:
                    # seq = self.get_sequence(table_id)
                    # pos = table[table_id]
                    table[table_id] = -1 # -(len(seq[pos:])-1)
                    resets += res
                continue

            _matches, t_values = res

            table.update(t_values)

            # for _table_id, t_value in _matches:
            #     # table[_table_id] = t_value
            #     matches += (_table_id,)
            matches += tuple(x[0] for x in _matches)

        return _hots, matches, resets

    def _test_insert_key(self, char, table_id, pos, table):
        seq = self.get_sequence(table_id)
        index_match = self._test_index_match(seq, pos, char, table_id)

        if index_match == 0:
            return False, (table_id, )

        return True, self._position_match(table, table_id, index_match, seq, char)

    def _test_index_match(self, seq, pos, char, table_id):
        """assert if the seq[pos] == char. Return the integer of the match as
        0 or 1
        """
        try:
            table_position = seq[pos]
        except IndexError:
            # The position is past the edge of the given sequence
            # This occurs when a key completes (has matched)
            # print('IndexError for', pos, 'on', table_id)
            index_match = seq[0] == char
            return int(index_match)

        index_match = table_position == char
        if isfunction(table_position):
            index_match = table_position(char)

        return int(index_match)

    def _position_match(self, table, table_id, index_match, seq, char):
        # The given char does match the current sequence position,
        # advance the index (usually by 1) and test for a completion
        # match.
        matches = ()
        t_value = table[table_id] + int(index_match)
        len_match = t_value >= len(seq)
        item = (table_id, t_value)

        if len_match:
            # table[table_id] = int(seq[0] == char)
            t_value = int(seq[0] == char)
            item = (table_id, t_value)
            # A sequence is complete, present a match,
            matches = (item,)
        # becomes `table[table_id] = t_value`
        table_updates = (item,)

        return matches, table_updates

