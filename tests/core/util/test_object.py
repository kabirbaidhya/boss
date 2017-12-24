''' Tests for boss.core.util.object module. '''

from boss.core.util.object import merge


def test_merge_v0():
    '''
    Test for boss.util.merge()
    Assert expected merge outcome when no conflicting keys are present.
    '''
    dict1 = {
        'key1': 'value1',
        'key2': {
            'key3': 'value3',
            'key4': 'value4'
        }
    }

    dict2 = {
        'keyA': 'valueA',
        'key2': {
            'keyB': 'valueB'
        }
    }

    expectedmerge = {
        'key1': 'value1',
        'key2': {
            'keyB': 'valueB',
            'key3': 'value3',
            'key4': 'value4'
        },
        'keyA': 'valueA'
    }

    merged = merge(dict1, dict2)

    assert merged == expectedmerge


def test_merge_v1():
    '''
    Test for boss.util.merge()
    Assert that second dictionary overrides conflicting keys during merge
    '''
    dict1 = {
        'key1': 'value1',
        'key2': {
            'key3': 'value3',
            'key4': 'value4'
        }
    }

    dict2 = {
        'key1': 'valueA',
        'key2': {
            'keyB': 'valueB'
        }
    }

    expectedmerge = {
        'key1': 'valueA',
        'key2': {
            'keyB': 'valueB',
            'key3': 'value3',
            'key4': 'value4'
        },
    }

    merged = merge(dict1, dict2)

    assert merged == expectedmerge
