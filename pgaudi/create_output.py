#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to generate the two global output file: .gaudi-output and .gaudi-log.
"""

import os
import gaudi
import yaml

from time import strftime


def merge_log(pcfgs, cfg):
    """
    Function to merge the .gaudi-log files of the different subprocesses.

    Arguments
    ---------
    pcfgs, cfg : gaudi.parse.Settings
        gaudi.parse.Settings objects for the yaml files of the subprocess and the main process (input file) respectively.

    """

    log_files = [
        os.path.join(pcfg.output.path, pcfg.output.name + ".gaudi-log")
        for pcfg in pcfgs
    ]
    gaudi_log = os.path.join(cfg.output.path, cfg.output.name + ".gaudi-log")
    with open(gaudi_log, "w") as log:
        log.write("Merged log files\n################\n\n")

        for logf in log_files:
            log.write(os.path.basename(logf) + ":\n***\n")

            with open(logf, "r") as f:
                for line in f.readlines():
                    log.write(line)

            log.write("\n")


def generate_out(population, cfg):
    """
    Function to write the global .gaudi-output file.

    Arguments
    ---------
    population : list
        List of unique individuals.
    cfg : gaudi.parse.Settings
        gaudi.parse.Settings object of the main process (the input file).

    """

    results = {
        "GAUDI.objectives": [
            "{} ({})".format(obj.name, obj.module) for obj in cfg.objectives
        ]
    }
    results["GAUDI.results"] = {}
    for ind in population:
        name = ind["name"] + ".zip"
        results["GAUDI.results"][name] = map(float, ind["score"])
    gaudi_output = os.path.join(cfg.output.path, cfg.output.name + ".gaudi-output")
    with open(gaudi_output, "w+") as out:
        out.write(
            "# Generated by GAUDI v{} on {}\n\n".format(
                gaudi.__version__, strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        out.write(yaml.safe_dump(results, default_flow_style=False))
