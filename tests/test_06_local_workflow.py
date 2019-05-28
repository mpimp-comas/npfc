"""
tests.test_06_local_workflow
~~~~~~~~~~
Functional test to make sure all step input/outputs are compatible
for a local run of the npfc workflow.
"""
# standard library
import logging
import subprocess
from pathlib import Path
# debug
# logging.basicConfig(level=logging.DEBUG)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def test_init_folder():
    """Removes all files in tmp worklow output folder"""
    for f in [x for x in Path('tests/tmp/local_workflow').iterdir() if x.is_file()]:
        f.unlink()


def test_run_local_workflow():
    """Run the local workflow defined in tests/data"""
    subprocess.run("snakemake -s tests/local_workflow.smk", shell=True, check=True)
    assert Path("tests/tmp/local_workflow/local_workflow.png").exists()
    assert Path("tests/tmp/local_workflow/data/chembl_small_001_map_crms.csv.gz").exists()
