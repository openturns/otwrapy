import otwrapy.examples.beam as ex_beam
import otwrapy as otw
import openturns as ot
import multiprocessing
import pytest

try:
    import pathos
    have_pathos = True
except ImportError:
    have_pathos = False

try:
    import ipyparallel
    have_ipyparallel = True
except ImportError:
    have_ipyparallel = False


def backendtest(backend):
    n_cpu = multiprocessing.cpu_count()
    sizes = [1, n_cpu, n_cpu + 1]
    if n_cpu > 2:
        sizes.append(n_cpu - 1)
    if n_cpu > 3:
        sizes.append(n_cpu - 2)
    model = ex_beam.Wrapper(sleep=0.2)
    if backend == "dask":
        dask_args = {"scheduler": "localhost", "workers": {"localhost": n_cpu}}
    else:
        dask_args = None
    model_parallel = otw.Parallelizer(model, backend=backend,
                                      n_cpus=n_cpu, dask_args=dask_args)
    for size in sizes:
        X_sample = ex_beam.distribution.getSample(size)
        Y_ref = model(X_sample)
        Y_sample = ot.Sample(model_parallel(X_sample))
        assert Y_ref == Y_sample, "samples do not match"


def test_serial():
    backendtest("serial")


def test_joblib():
    backendtest("joblib")


def test_multiprocessing():
    backendtest("multiprocessing")


@pytest.mark.skipif(not have_ipyparallel, reason="N/A")
def test_ipython():
    backendtest("ipyparallel")


@pytest.mark.skipif(not have_pathos, reason="N/A")
def test_pathos():
    backendtest("pathos")


@pytest.mark.skip(reason="needs passwordless ssh configuration")
def test_dask():
    backendtest("dask/ssh")
