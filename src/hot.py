

class HotMixin(object):
    # # keys are not pulled from the hot key list if they are
    # # in sleeping
    # # (The position int is < -1
    # # denoting a drop of distance
    # # from the tip (the match))
    # respect_sleeping = True

    def set_next_hots(self, char):
        """Given a char, step the val if it exists in the 'hot start'

        The hots dict, applied the first item of the sequence to each
        mapped key; speeding up initial steps into an open sequence
            {
                "w": {'w', 'win', 'window'}
                "c": {'cape'}
            }
        """

        hot_keys = self.get_hot_keys(char)

        hot_starts = set()
        # Iterate all table ids found in the hot start table,
        # where the hot-start key is the given char.
        for table_id in hot_keys:
            # if self.is_sleeping(table_id):
            #     pos = self.get_position(table_id)
            #     print('Skip sleeping', table_id, pos, 'for', char)
            if self._apply_hot_position(table_id, char):
                # an event response to the insert function.
                hot_starts.add(table_id)

        return tuple(hot_starts)

    # def is_sleeping(self, table_id):
    #     pos = self.get_position(table_id)
    #     return pos < -1 # lower than -1 is sleeping distance

    def get_hot_keys(self, char):
        """Return all table ids matching the given `char` id.
        """
        r = self.hots.get(char, None) or ()
        for table_id, functions in self.hot_functions.items():
            for f in functions:
                if f(char):
                    r += (table_id, )
                    break # first success.
        return r

    def install_hot_key(self, value, table_id):
        """Apply the given `value` as a hot key for the given `table_id`.

        This applies the value as the _start_ of the sequeunce, used to check
        if a sequence should start without iterating all available sequences.

        returns None
        """
        if callable(value):
            self.hot_functions[table_id].add(value)
        self.hots[value].add(table_id)

    def _apply_hot_position(self, table_id, char):
        # Find the current position of the sequence running index.
        pos = self.get_position(table_id)
        sequence = self.get_sequence(table_id)
        not_is_match = not self._is_gt_1_position_match(sequence, pos, char)

        if not_is_match:
            # Reset to zero - applying the new position as open.
            self.set_position(table_id, 0)

        # If the current char is a match within the sequence (where pos > 1)
        # then is not a hot-start, as the sequence is already running.
        return not_is_match

    def _is_gt_1_position_match(self, sequence, pos, char):
        """Given a sequence, an expected position within the sequence,
        and a matching `char`, test if the char matches the value at the
        seq[pos]. Only do this if pos is greater than 1.

        return bool - True for a match of the char to the seq[pos]
                      where `pos > 1`, else False.
        """
        if pos >= 1:
            # This position is already open but the start char (table_id)
            # matches the given (char). This may occur for dup index words
            # such as "window" or "ddddddd"
            try:
                # Don't reset to zero because this is already open.
                # and the key matches the current sequece (an open step.)
                value = sequence[pos]
                return value == char
            except IndexError:
                # The key does not exist at this position,
                # thus the given (char), must be the first index.
                pass
        return False

