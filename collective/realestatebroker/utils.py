"""Utility functions for realestatebroker."""

def batch(items, batch_size=5, selected=0):
    """Return a batch of photos.

    >>> from collective.realestatebroker.utils import batch

    Test whether we're returning max 5 items.

    >>> result = batch([])
    >>> result
    False
    >>> result = batch(range(5))
    >>> [i['item'] for i in result['items']]
    [0, 1, 2, 3, 4]
    >>> result = batch(range(200))
    >>> [i['item'] for i in result['items']]
    [0, 1, 2, 3, 4]

    The selected item is also returned:

    >>> result['selected']
    0

    If we do it with strings, the result is clearer.

    >>> string_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']
    >>> result = batch(string_list)
    >>> result['selected']
    'one'

    If the selected index is too big or too small, it is restricted to
    available values.

    >>> result = batch(string_list, selected=-10)
    >>> result['selected']
    'one'
    >>> result = batch(string_list, selected=100)
    >>> result['selected']
    'seven'

    Forward/reverse points at +/-1, compensated for the length of the items.

    >>> result = batch(string_list, selected=0)
    >>> result['reverse'] # Already at start, returns None
    >>> result['forward']
    1
    >>> result = batch(string_list, selected=4)
    >>> result['reverse']
    3
    >>> result['forward']
    5
    >>> result = batch(string_list, selected=6)
    >>> result['reverse']
    5
    >>> result['forward'] # Already at end, returns None

    Fast forward/reverse is more involved. If the item to jump to is already
    displayed, return None instead (to disable it). Also the jump has to be
    big enough to compensate for items at the start/end of the sequence.

    >>> result = batch(range(100), selected=50)
    >>> result['fastreverse']
    45
    >>> result['fastforward']
    55

    If we're at 'one', 'three' is in the center (index=2). So a jump by 5
    would put us at index=7, which is out of reach. So index=6 must be the
    selected item.

    >>> result = batch(string_list, selected=0)
    >>> result['fastreverse']
    >>> result['fastforward']
    6

    Additionally, the selected item's dict must be marked as such.
    >>> result['items'][0]['selected']
    True
    >>> result['items'][1]['selected']
    False

    If possible, the selected item should be centered.

    >>> result = batch(range(10), selected=4)
    >>> [i['item'] for i in result['items']]
    [2, 3, 4, 5, 6]


    """
    result = {}
    margin = batch_size // 2 # Integer
    # Pack the items as a list of dicts.
    items = list(items)
    # Fix up selected as it can be too big or too small.
    if len(items) == 0:
        return False
    if selected < 0:
        selected = 0
    if selected >= len(items):
        selected = len(items) - 1
    # Determine start/end values.
    start = selected - margin
    if start < 0:
        start = 0
        end = batch_size
    else:
        end = selected + margin + 1
    if end >= len(items):
        end = len(items)
    # Decorate items
    result['items'] = []
    for index, item in enumerate(items[start:end]):
        item_dict = {'item': item,
                     'index': index,
                     'selected': index == selected}
        result['items'].append(item_dict)
    # For ease of use, explicitly include the selected item.
    result['selected'] = items[selected]
    # Calculate (fast) forward and reverse indexes.
    result['reverse'] = _only_in_range(items, selected-1)
    result['forward'] = _only_in_range(items, selected+1)
    centered = selected
    if centered - margin < 0:
        centered = 0 + margin
    if centered +margin >= len(items):
        centered = len(items) - 1 - margin
    result['fastreverse'] = _only_in_range(items, centered-batch_size)
    result['fastforward'] = _only_in_range(items, centered+batch_size)
    if not result['fastreverse']:
        result['fastreverse'] = _only_in_range(items, centered-batch_size,
                                               margin=margin)
    if not result['fastforward']:
        result['fastforward'] = _only_in_range(items, centered+batch_size,
                                               margin=margin)
    return result


def _only_in_range(items, index, margin=0):
    # Helper method for batch()
    if index < 0:
        if index + margin < 0:
            return None
        return 0
    if index >= len(items):
        if index - margin >= len(items):
            return None
        return len(items) - 1
    return index
