import os
import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Get all the noteboooks in each folder
# Notebooks with names starting large_ contain very large problems so are skipped
notebooks = []
for dir in ["laplace", "helmholtz", "maxwell"]:
    for i in os.listdir(os.path.join("notebooks", dir)):
        if i.endswith(".ipynb") and not i.startswith("large_"):
            notebooks.append((os.path.join("notebooks", dir), i))

kernel = "python3"
if "KERNEL_NAME" in os.environ:
    kernel = os.environ["KERNEL_NAME"]


@pytest.mark.parametrize('kernel_name', [kernel])
@pytest.mark.parametrize(('path', 'notebook'), notebooks)
def test_notebook(path, notebook, kernel_name):
    with open(os.path.join(path, notebook)) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)

    ep.preprocess(nb, {'metadata': {'path': path}})
