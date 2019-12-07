from global_app.templatetags.utils import sum_of, split


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
        assert  ['2', 'million'] == split('2 million')

    def test_diffent_separator(self):
        assert  ['2', 'million'] == split('2-million', sep='-')
        assert  ['2 million'] == split('2 million', sep='-')
