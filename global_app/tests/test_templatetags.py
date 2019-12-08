from global_app.templatetags.utils import sum_of, split
from global_app.templatetags.format import small_intword


class TestSumOf:
    def test_base(self):
        iterable = [dict(a=1), dict(a=2), dict(a=3)]
        assert 6 == sum_of(iterable, 'a')

    def test_all_zeroes(self):
        iterable = [dict(a=0), dict(a=0), dict(a=0)]
        assert 0 == sum_of(iterable, 'a')

    def test_missing_attr(self):
        iterable = [dict(a=1), dict(a=2), dict(a=3)]
        assert None == sum_of(iterable, 'missing_key')


class TestSplit:
    def test_base(self):
        assert ['2', 'million'] == split('2 million')

    def test_diffent_separator(self):
        assert ['2', 'million'] == split('2-million', sep='-')
        assert ['2 million'] == split('2 million', sep='-')

    def test_ignore_non_str(self):
        assert [2] == split(2)
        assert [42] == split(42)


class TestSmallIntWord:
    def test_big_numbers(self):
        assert '2,0 milhões' == small_intword(2000000)

    def test_thousands(self):
        assert '2,2 mil' == small_intword(2200)

    def test_small_numbers(self):
        assert 200 == small_intword(200)
        assert 2 == small_intword(2)

    def test_do_nothing_if_it_is_not_a_number(self):
        assert 'not a number' == small_intword('not a number')
