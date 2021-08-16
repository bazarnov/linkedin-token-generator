#
# MIT License
#
# Copyright (c) 2021 Oleksandr Bazarnov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import argparse
import importlib
import os.path
import sys
import json
from typing import Dict, List, Mapping, Any

from linkedin_token.modules import LinkedInAuth

class Entrypoint(object):
    def __init__(self, source: LinkedInAuth):
        self.source = source

    def parse_args(self, args: List[str]) -> argparse.Namespace:
        # set up parent parsers
        parent_parser = argparse.ArgumentParser(add_help=False)
        main_parser = argparse.ArgumentParser()
        subparsers = main_parser.add_subparsers(title="commands", dest="command")

        # generate
        generate_parser = subparsers.add_parser("generate", help="Generates 2-months Access_Token for the linkedIn Ads/Marketing ", parents=[parent_parser])
        req_generate_parser = generate_parser.add_argument_group("required named arguments")
        req_generate_parser.add_argument("--config", type=str, required=True, help="path to the json configuration file")

        return main_parser.parse_args(args)

    def run(self, parsed_args: argparse.Namespace) -> Dict:
        cmd = parsed_args.command
        if not cmd:
            raise Exception("No command passed")
        # read the config
        config = read_config(parsed_args.config)
        if cmd == "generate":
            return self.source.get_access_token(config)
        else:
            raise Exception("Unexpected command " + cmd)


def read_config(config_path: str) -> Mapping[str, Any]:
    with open(config_path, "r") as file:
        contents = file.read()
    return json.loads(contents)

def launch(source: LinkedInAuth, args: List[str]):
    print(Entrypoint(source).run(Entrypoint(source).parse_args(args)))

def main():
    impl_module = os.environ.get(LinkedInAuth.__module__)
    impl_class = os.environ.get(LinkedInAuth.__name__)
    module = importlib.import_module(impl_module)
    impl = getattr(module, impl_class)
    # set up and run entrypoint
    source = impl()
    launch(source, sys.argv[1:])
