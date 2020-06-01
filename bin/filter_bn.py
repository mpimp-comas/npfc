"""
Script filter_bn
==========================
This is quick and dirty script to filter out benzene fragment hits from DNP/ChEMBL runs (fsearch).

It creates a new folder next to the specified input fragment subdir (i.e. frags_crms, frags_crms_nobn)


"""

from pathlib import Path
import re
import argparse
from datetime import datetime
import npfc
from npfc import load
from npfc import save
from npfc import utils
import sys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def filter_fragments(input_file, output_file, idfs=['32']):

    df = load.file(input_file, decode=False)
    df = df[~df['idf'].isin(idfs)]
    save.file(df, output_file, encode=False)

    return len(df)

def edit_log(log_in, log_out, new_count):
    """This function is not smart at all and just helps me remember which data files were edited.
    I just add a header to the log file stating that it was modified.
    """
    reading_file = open(log_in, "r")
    new_file_content = ""

    for line in reading_file:
        stripped_line = line.strip()
        new_line = stripped_line
        new_line = re.sub('RUNNING', "RUNNING (EDITED!!!)", new_line)
        new_line = re.sub('FOUND [0-9]+ HITS', f"FOUND {new_count} HITS", new_line)
        new_line = re.sub('SAVED [0-9]+ RECORDS', f"SAVED {new_count} RECORDS", new_line)
        new_file_content += new_line + "\n"

    reading_file.close()
    writing_file = open(log_out, "w+")
    writing_file.write(new_file_content)
    writing_file.close()


def main():

    # init
    d0 = datetime.now()
    description = """Script used to filter out benzene fragment hits from DNP/ChEMBL runs (fsearch).

    It creates a new folder next to the specified input fragment subdir (i.e. frags_crms, frags_crms_nobn)

    It uses the installed npfc libary in your favorite env manager.

    Example:

        >>> filter_bn frags_crms frags_crms_nobn

    """

    # parameters CLI
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_frags_subdir', type=str, default=None, help="Input file for fragment combinations.")
    parser.add_argument('output_frags_subdir', type=str, default=None, help="Output file basename. It gets appended with the type of output being produced: raw, clean and map.")
    parser.add_argument('--log', type=str, default='INFO', help="Specify level of logging. Possible values are: CRITICAL, ERROR, WARNING, INFO, DEBUG.")
    args = parser.parse_args()

    # logging
    logger = utils._configure_logger(args.log)
    logger.info("RUNNING FILTER_BN")
    d0 = datetime.now()
    pad = 40

    # parse arguments
    utils.check_arg_input_dir(args.input_frags_subdir)
    utils.check_arg_output_dir(args.output_frags_subdir)

    # WD_IN
    WD_IN = args.input_frags_subdir  # the frags_xxxx subfolder in the relevent dataset folder tree
    WD_OUT = args.output_frags_subdir

    # GET STEPS
    steps = sorted([d for d in Path(WD_IN).glob('*') if d.is_dir()])
    step = [x for x in steps if x.name.endswith('fsearch')][0]

    # display infos
    logger.info("LIBRARY VERSIONS:")
    logger.info("npfc".ljust(pad) + f"{npfc.__version__}")
    logger.info("ARGUMENTS:")
    logger.info('INPUT FRAGS SUBDIR'.ljust(pad) + f"{WD_IN}")
    logger.info('OUTPUT FRAGS SUBDIR'.ljust(pad) + f"{WD_OUT}")
    logger.info('STEP'.ljust(pad) + f"{step}")
    logger.info("LOG".ljust(pad) + f"{args.log}")

    # BEGIN
    logger.info("RUNNING FILTER BN")

    logger.info(f"\nPROCESSING: {step.name}")
    new_counts = []
    WD_OUT_LOG_p = Path(f"{WD_OUT}/{step.name}/log")
    if not WD_OUT_LOG_p.exists():
        WD_OUT_LOG_p.mkdir(parents=True, exist_ok=True)

    # data
    logger.info("NOW UPDATING DATA...")
    chunks_in = sorted([x for x in step.glob('data/*')])
    chunks_out = [f"{WD_OUT}/{step.name}/data/{x.name}" for x in chunks_in]
    chunks = [(str(x), y) for x, y in zip(chunks_in, chunks_out)]
    for chunk_in, chunk_out in chunks:
        new_counts.append(filter_fragments(chunk_in, chunk_out))

    # logs
    logger.info("NOW UPDATING LOGS...")
    logs_in = sorted([x for x in step.glob('log/*log')])
    logs_out = [f"{WD_OUT}/{step.name}/log/{x.name}" for x in logs_in]
    logs = [(str(x), y, new_count) for x, y, new_count in zip(logs_in, logs_out, new_counts)]
    for log_in, log_out, new_count in logs:
        edit_log(log_in, log_out, new_count)

    d1 = datetime.now()
    logger.info("COMPUTATIONAL TIME: TOTAL".ljust(pad * 2) + f"{d1-d0}")
    logger.info("END")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


if __name__ == '__main__':
    main()
    sys.exit(0)
