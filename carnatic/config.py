from settings import *
import configparser
from enum import Enum
import csv


config = configparser.ConfigParser()
settings = config.read(GLOBAL_CONSTANTS_FILE)


if __name__ == '__main__':
    
    settings = get_settings_from_file(GLOBAL_CONSTANTS_FILE)
    print(settings)
    key = 'scale_of_notes'
    print(key+"=",settings[key])
    print(SCALE_OF_NOTES)
    raaga_dict = get_raaga_dictionary()
    print(RAAGA_NAMES)
                                  