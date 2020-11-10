#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  #
#  Carnatic Music Guru (PyCarnatic)                                                              #
#  Copyright © 2020 Sundar Sundaresan <Sundaram.Sundaresan@gmail.com>.                           #
#                                                                                                #
#  This program is free software: you can redistribute it and/or modify it under the terms of    #
#  the GNU General Public License as published by the Free Software Foundation, either version   #
#  3 of the License, or (at your option) any later version.                                      #
#                                                                                                #
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;     #
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.     #
#  See the GNU General Public License for more details.                                          #
#                                                                                                #
#  You should have received a copy of the GNU General Public License along with this program.    #
#  If not, see <http://www.gnu.org/licenses/>.                                                   #
#  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  #

name = "carnatic"

version = "0.8.0"

author = "Sundar Sundaresan"

author_email = "Sundaram.Sundaresan@gmail.com"

description = "A Python package for generating Carnatic music lessons for about 400 raagas and 35 thaaLas, "\
            "generating music according to the carnatic note notations in a file and supports " \
              "carnatic insutrments such as Veena, Veena2, Flute, Violin etc, and " \
              "adds percussion layer (Mridangam or EastWestMix) according to the specified thaaLa."

url = "https://github.com/naturalstupid/pycarnatic"

project_urls = {
    "Source Code": "https://github.com/naturalstupid/pycarnatic",
    "Documentation": "https://github.com/naturalstupid/pycarnatic",
}

install_requires = ['itertools', "configparser", 'operator', 'collections', 'enum', 'csv', 'numpy', 'scamp', 'math', 're', 'regex', 'random',]

#extras_require = { }

package_data = {
    'carnatic': ['config/*', 'config/*/*', 'Lib/*', 'Lessons/*', 'Lessons/*/*','Notes/*', 'tmp/*', 'model_weights/*']
}

classifiers = [
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]
