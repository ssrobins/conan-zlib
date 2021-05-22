#!/usr/bin/env python3

import argparse
import os.path
import subprocess

def main():
    platform = {
        "androidarm": "-s os=Android -s os.api_level=16 -s arch=armv7 -s compiler=clang -s compiler.version=11 -s compiler.libcxx=libc++",
        "androidarm64": "-s os=Android -s os.api_level=21 -s arch=armv8 -s compiler=clang -s compiler.version=11 -s compiler.libcxx=libc++",
        "ios": "-s os=iOS -s arch=armv7 -s os.version=9.0 -s compiler.version=12.0",
        "linux": "-s compiler.libcxx=libstdc++11",
        "macos": "-s os.version=10.9 -s compiler.version=12.0",
        "windows": "-s arch=x86 -s compiler.version=16 -s compiler.runtime=MT"
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=list(platform.keys()), help="Build platform")
    command_args = parser.parse_args()

    script_path = os.path.dirname(os.path.realpath(__file__))

    remote_url = "https://ssrobins.jfrog.io/artifactory/api/conan/conan"
    subprocess.run(f"conan remote add artifactory-ssrobins {remote_url} --insert --force",
        cwd=script_path, shell=True, check=True)

    subprocess.run(f"conan create --update . {platform[command_args.platform]}",
        cwd=script_path, shell=True, check=True)


if __name__ == "__main__":
    main()
