#
# ESPRESSIF MIT License
#
# Copyright (c) 2020 <ESPRESSIF SYSTEMS (SHANGHAI) PTE LTD>
#
# Permission is hereby granted for use on ESPRESSIF SYSTEMS ESP32 only, in which case,
# it is free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os
import sys
import stat
import argparse
import subprocess

def main():
    """ main """
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_dir", default=".", help="project path")
    parser.add_argument("--tools_dir", default=".", help="the tools directory")
    parser.add_argument("--output_dir", default="output", help="the output bin directory")
    parser.add_argument("--flash_args_file", default="flash_args_file", help="the file to store flash args")
    args = parser.parse_args()

    project_dir = args.project_dir.strip()
    tools_dir = args.tools_dir.strip()
    output_dir = args.output_dir.strip()
    flash_args_file = args.flash_args_file.strip()

    # print('tools_dir={}'.format(tools_dir))
    # print('output_dir={}'.format(output_dir))
    # print('flash_args_file={}'.format(flash_args_file))

    # if sys.platform.startswith('win32'):
    #     tools_dir = tools_dir.replace(r'\/'.replace(os.sep, ''), os.sep)
    #     output_dir = output_dir.replace(r'\/'.replace(os.sep, ''), os.sep)
    #     flash_args_file = flash_args_file.replace(r'\/'.replace(os.sep, ''), os.sep)

    # print('tools_dir1={}'.format(tools_dir))
    # print('output_dir1={}'.format(output_dir))
    # print('flash_args1_file={}'.format(flash_args_file))

    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)

    with open(flash_args_file, 'r') as args_file:
        for line in args_file.readlines():
            line_str = line.strip()
            if line_str != '':
                str_list = line_str.split(' ')
                full_filename = str_list[1]
                file_size = str_list[2]
                file_name = os.path.basename(full_filename)
                partition_name = os.path.splitext(file_name)[0]
                tool_name = os.path.join(tools_dir, ''.join([partition_name, '.py']))
                if not os.access(tool_name, os.X_OK):
                    os.chmod(tool_name, stat.S_IRUSR | stat.S_IXUSR)

                # if sys.platform.startswith('win32'):
                #     tool_name = tool_name.replace(r'\/'.replace(os.sep, ''), os.sep)
                ret = subprocess.call([sys.executable, tool_name, '--partition_name', partition_name, '--partition_size', file_size, '--outdir', output_dir, '--project_path', project_dir], shell = False)


if __name__ == '__main__':
    main()