
def single_frames(sequences, iterable):
    """ Push many chars into the sequence and render many single frames,
    returning the last (current) result from the iteration

    Functionally, this affects the sequence table in the same manner as "mass_frame"
    but yields _the last_ result:

        ?: window
        # ... 5 more frames.

        WORD    POS  | NEXT | STRT | OPEN | HIT  | DROP
        apples       |      |      |      |      |
        window   1   |  i   |      |  #   |  #   |
        ape          |      |      |      |      |
        apex         |      |      |      |      |
        extra        |      |      |      |      |
        tracks       |      |      |      |      |
        stack        |      |      |      |      |
        yes          |      |      |      |      |
        cape         |      |      |      |      |
        cake         |      |      |      |      |
        echo         |      |      |      |      |
        win      1   |  i   |  #   |  #   |      |
        wind     1   |  i   |  #   |  #   |      |
        windy    1   |  i   |  #   |  #   |      |
        w        1   |      |  #   |  #   |  #   |
        ww       1   |  w   |  #   |  #   |      |
        ddddd        |      |      |      |      |

          (
            ('win', 'ww', 'wind', 'w', 'windy'),
            ('window', 'w'),
            ()
          )
    """
    return sequences.table_insert_keys(iterable)


def mass_frame(sequences, iterable):
    """
    Push many chars into the sequence and return a concat of all starts, hits,
    and drops for the iterable.

        ?: window

        WORD    POS  | NEXT | STRT | OPEN | HIT  | DROP
        apples       |      |      |      |      |
        window   1   |  i   |  #   |  #   |  #   |
        ape          |      |      |      |      |
        apex         |      |      |      |      |
        extra        |      |      |      |      |
        tracks       |      |      |      |      |
        stack        |      |      |      |      |
        yes          |      |      |      |      |
        cape         |      |      |      |      |
        cake         |      |      |      |      |
        echo         |      |      |      |      |
        win      1   |  i   |  #   |  #   |  #   |  #
        wind     1   |  i   |  #   |  #   |  #   |  #
        windy    1   |  i   |  #   |  #   |      |  #
        w        1   |      |  #   |  #   |  #   |  #
        ww       1   |  w   |  #   |  #   |      |  #
        ddddd        |      |  #   |      |      |  #

        ( ('ww', 'windy', 'win', 'wind', 'w', 'window', 'ddddd', 'ww', 'windy',
            'win', 'wind', 'w'),
          ('w', 'win', 'wind', 'window', 'w'),
          ('w', 'ww', 'win', 'wind', 'windy', 'ddddd')
        )

    This is useful for mass framing:

        V:apextrackstackcapechoappleswwindowwindyyescakedddddf
        IndexError for 1 on w
        IndexError for 1 on w

          WORD    POS  | NEXT | STRT | OPEN | HIT  | DROP
          apples       |      |  #   |      |  #   |  #
          window       |      |  #   |      |  #   |  #
          ape          |      |  #   |      |  #   |  #
          apex         |      |  #   |      |  #   |  #
          extra        |      |  #   |      |  #   |  #
          tracks       |      |  #   |      |  #   |  #
          stack        |      |  #   |      |  #   |  #
          yes          |      |  #   |      |  #   |  #
          cape         |      |  #   |      |  #   |  #
          cake         |      |  #   |      |  #   |  #
          echo         |      |  #   |      |  #   |  #
          win          |      |  #   |      |  #   |  #
          wind         |      |  #   |      |  #   |  #
          windy        |      |  #   |      |  #   |  #
          w            |      |  #   |      |  #   |  #
          ww           |      |  #   |      |  #   |  #
          ddddd        |      |  #   |      |  #   |  #
    """
    trip = sequences.insert_keys(*iterable)
    sequences.print_state_table(*trip)
    return trip

