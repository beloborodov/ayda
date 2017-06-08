from itertools import chain


class AYDA(object):

    def __init__(self, count=100):
        self.train = {}
        self.count = count

    def fit(self, train):
        self.train = {
            k: [(rec, clk)
                for rec, clk in v
                if not (rec in u or u.add(rec))]
            for k, v, u in ((k, v, set())
                            for k, v in reduce(lambda d, (i, j, clk):
                                                      d.setdefault(i, []).append((j, clk)) or d,
                                               chain.from_iterable(
                                                    [
                                                        chain([(tr, k, v) for k, v in rec],
                                                              [(k, tr, v) for k, v in rec],
                                                              [(k1, k2, v1)
                                                               for k1, v1 in rec
                                                               for k2, v2 in rec
                                                               if k1 != k2])
                                                        for tr, rec in ((t['item'],
                                                                         t['true_recoms'].items())
                                                                        for t in train
                                                                        if t['item'])
                                                    ]
                                                ),
                                                {}
                                        ).iteritems()
                           )
        }
        return self

    def tranform(self, test_ids):
        test_ids_set = set(test_ids)
        return {
            k: {rec: self.count - n
                for n, rec in enumerate([rec
                                         for rec, clk in (chain(v,
                                                                chain.from_iterable([self.train.get(rec, [])
                                                                                     for rec, clk in v])))
                                         if not (rec in u or u.add(rec))
                ][:self.count])
            }
            for k ,v, u in ((k, v, set())
                            for k, v in ((k, v)
                                              for k, v in self.train.iteritems()
                                              if k in test_ids_set)
                            )
        }
