import openturns as ot
import otwrapy as otw
import os
import shutil


def test_tempworkdir():
    for cleanup in [True, False]:
        with otw.TempWorkDir(cleanup=cleanup) as cwd:
            print(cwd)
            assert os.path.exists(cwd), "temp dir should exist"
        if cleanup:
            assert not os.path.exists(cwd), "temp dir should not persist"
        else:
            assert os.path.exists(cwd), "temp dir should persist"
            shutil.rmtree(cwd)


def test_array_serialization():
    sample = ot.Normal(5).getSample(100)
    for compress in [True, False]:
        with otw.TempWorkDir(cleanup=True) as cwd:
            fn = os.path.join(cwd, "x.bin")
            otw.dump_array(sample, fn, compress=compress)
            sample2 = otw.load_array(fn, compressed=compress)
            assert sample == sample2, "samples should be identical"


def test_array_safemakedirs():
    for existing in [True, False]:
        with otw.TempWorkDir(cleanup=True) as cwd:
            dn = os.path.join(cwd, "foo")
            if existing:
                os.makedirs(dn)
            otw.safemakedirs(dn)
            assert os.path.exists(dn), "dir should exist"
