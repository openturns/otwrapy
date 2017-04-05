from __future__ import print_function
from otwrapy.examples.beam import Wrapper, X_distribution
import otwrapy as otw
import openturns as ot
import multiprocessing

def backendtest(backend):
    ot.RandomGenerator.SetSeed(0)
    n_cpu = multiprocessing.cpu_count()
    sizes = [1, n_cpu, n_cpu + 1]
    if n_cpu > 2:
        sizes.append(n_cpu - 1)
    if n_cpu > 3:
        sizes.append(n_cpu - 2)
    model = Wrapper(sleep=0.2)
    model_parallel = otw.Parallelizer(model, backend=backend)
    for size in sizes:
        X_sample = X_distribution.getSample(size)
        Y_ref = model(X_sample)
        Y_sample = ot.Sample(model_parallel(X_sample))
        assert Y_ref == Y_sample, 'samples do not match'

def test_joblib():
    backendtest('joblib')

def test_multiprocessing():
    backendtest('multiprocessing')

def test_ipython():
    backendtest('ipython')

def test_pathos():
    backendtest('pathos')
