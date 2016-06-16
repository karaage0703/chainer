import unittest

import numpy

import chainer
from chainer import cuda
from chainer import functions
from chainer import gradient_check
from chainer import testing
from chainer.testing import attr


@testing.parameterize(*testing.product_dict(
    [
        {'shape': (3, 4), 'axis': 0},
        {'shape': (3, 4), 'axis': 1},
        {'shape': (3, 4), 'axis': 2},
        {'shape': (3, 4), 'axis': -1},
        {'shape': (), 'axis': 0},
        {'shape': (), 'axis': -1},
    ],
    [
        {'dtype': numpy.float16},
        {'dtype': numpy.float32},
        {'dtype': numpy.float64},
    ]
))
class TestStack(unittest.TestCase):

    def setUp(self):
        self.xs = [numpy.random.uniform(-1, 1, self.shape).astype(self.dtype)]

    def check_forward(self, xs_data):
        xs = [chainer.Variable(x) for x in xs_data]
        y = functions.stack(xs, axis=self.axis)

        if hasattr(numpy, 'stack'):
            # run test only with numpy>=1.10
            expect = numpy.stack(self.xs, axis=self.axis)
            gradient_check.assert_allclose(y.data, expect)

    def test_forward_cpu(self):
        self.check_forward(self.xs)

    @attr.gpu
    def test_forward_gpu(self):
        self.check_forward([cuda.to_gpu(x) for x in self.xs])


testing.run_module(__name__, __file__)