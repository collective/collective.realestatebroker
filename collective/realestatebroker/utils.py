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
    >>> result['reverse']
    0
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
    >>> result['forward']
    6

    Fast forward/reverse is more involved. If the item to jump to is already
    displayed, return None instead (to disable it). Also the jump has to be
    big enough to compensate for items at the start/end of the sequence.




    """
    result = {}
    # Pack the items as a list of dicts.
    items = list(items)
    # Fix up selected as it can be too big or too small.
    if len(items) == 0:
        return False
    selected = _in_range(items, selected)
    # Determine start/end values.
    start = 0
    end = batch_size
    # Decorate items
    result['items'] = []
    for index, item in enumerate(items[start:end]):
        item_dict = {'item': item,
                     'index': index,
                     'selected': False}
        result['items'].append(item_dict)
    # For ease of use, explicitly include the selected item.
    result['selected'] = items[selected]
    # Calculate (fast) forward and reverse indexes.
    result['reverse'] = _in_range(items, selected-1)
    result['fastreverse'] = _in_range(items, selected-5)
    result['forward'] = _in_range(items, selected+1)
    result['fastforward'] = _in_range(items, selected+5)
    return result


def _in_range(items, index):
    # Helper method for batch()
    if index < 0:
        index = 0
    if index >= len(items):
        index = len(items) - 1
    return index
