import enum
import os
import pickle
import re
import subprocess


class Color(enum.Enum):
    BLACK = 90
    RED = 91
    GREEN = 92
    YELLOW = 93
    BLUE = 94
    MAGENTA = 95
    CYAN = 96
    WHITE = 97


def set_string_colored(printStr, colorVal):
    if type(colorVal) is str:
        print("Warning: set_string_colored(printStr, colorVal) - colorVal is int value. ex) Color.RED or 91")
        return printStr

    colorStr = '\033[' + str(colorVal) + 'm'
    endColorStr = '\033[0m'
    coloredStr = colorStr + printStr + endColorStr

    return coloredStr


def get_fileList_in_directory(dirPath):
    return os.listdir(dirPath)


def get_endpointDirList(dirPath):
    subDirList = get_subDirectoryList_in_directory(dirPath)
    endpointDirList = list()

    for subDir in subDirList:

        if is_endpoint_directory(subDir):
            endpointDirList.append(subDir)

    return endpointDirList


def get_subDirectoryList_in_directory(dirPath):
    findSubDir = subprocess.check_output("find " + dirPath + " -type d 2>/dev/null", shell=True)
    resultStr = convert_subprocess_output_to_str(findSubDir)
    subDirList = trim_newLines(resultStr)[:-1]

    return subDirList


def generate_directories_to_endpoint(endpointPath):
    if not is_path_exists(endpointPath):
        os.makedirs(endpointPath)


def replace_string_in_list(targetList, srcStr, dstStr):
    replacedList = list()

    for target in targetList:
        replacedList.append(target.replace(srcStr, dstStr))

    return replacedList


def run_shell_command(command):
    outputByte = subprocess.check_output(command, shell=True)
    outputStr = convert_subprocess_output_to_str(outputByte)

    return outputStr


def convert_subprocess_output_to_str(outputByte):
    resultStr = str(outputByte)
    resultStr = trim_quotationMarks(resultStr)[1]

    return resultStr


def trim_quotationMarks(inputStr):
    return inputStr.split("'")


def trim_newLines(inputStr):
    return inputStr.split("\\n")


def is_endpoint_directory(filePath):
    subFileList = get_fileList_in_directory(filePath)

    for subFile in subFileList:
        subFilePath = filePath + '/' + subFile

        if is_directory(subFilePath):
            return False

    return True


def is_directory(targetPath):
    return os.path.isdir(targetPath)


def is_path_exists(path):
    return os.path.exists(path)


def get_regex_index(targetList, regexStr):
    regex = re.compile(regexStr)
    idxList = [i for i, item in enumerate(targetList) if re.search(regex, item)]
    return idxList


def save_pickle(filePath, data):
    pickleFile = open(filePath, 'wb')
    pickle.dump(data, pickleFile)
    pickleFile.close()


def load_pickle(filePath):
    pickleFile = open(filePath, 'rb')
    loadedData = pickle.load(pickleFile)
    return loadedData


def remove_files(dirPath):
    fileList = os.listdir(dirPath)

    for file in fileList:
        filePath = dirPath + file
        os.remove(filePath)

