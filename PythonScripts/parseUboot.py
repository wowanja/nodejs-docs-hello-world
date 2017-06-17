import os
import argparse
import fullpaths
import re
from datetime import datetime
from junit_xml import TestSuite, TestCase


def save_testsuite_to_file(test_suite, output_filename):
    try:
        if not os.path.exists(os.path.dirname(output_filename)):
            try:
                os.makedirs(os.path.dirname(output_filename))
            except OSError as exc: # Guard against race condition
                print(exc)
                if exc.errno != errno.EEXIST:
                    raise
        with open(output_filename, 'w') as f:
            TestSuite.to_file(f, [test_suite], prettyprint=True)
    except Exception as ex:
        print(ex)

def processTestResult(input_filename, output_filename):

    test_suite_properties = {}

    with open(input_filename) as file:
        first_line = file.readline()
        first_line_entries = re.split('\s|\t| ', first_line)
        test_suite_name = first_line_entries[3]
        
        test_suite_timestamp = first_line_entries[4] + ' ' + first_line_entries[9]
        timestamp = datetime.strptime(test_suite_timestamp, '%d/%m/%Y %H:%M:%S').isoformat()
        
        second_line = file.readline()
        second_line_entries = re.split('\s|\t', second_line)
        test_suite_properties['Konfiguration'] = second_line_entries[1]
        
        third_line = file.readline()
        third_line_entries = re.split('Index: ', third_line.strip(' \t\n\r'))
        test_suite_properties['Index'] = third_line_entries[1].strip(' \t\n\r')

        for line in file: # skip lines until '-----'
            if (line.startswith('-----')):
                break
        
        test_cases = []
        for line in file:
            if (line.startswith('-----')): # end of tests is reached
                break
            
            line_entries = line.split(':')
            test_case_classname = line_entries[0]
            tmp_entries = line_entries[1].split('\t-')
            
            test_case_name = tmp_entries[0].strip(' \t\n\r')

            test_case_result = tmp_entries[1].strip(' \t\n\r')
            
            tc = TestCase(name=test_case_name, classname=test_case_classname)
            if (test_case_result.strip(' \t\n\r').lower() == 'not tested'):
                tc.add_skipped_info('Test SKIPPED', 'skipped output')
            if (test_case_result.strip(' \t\n\r').lower() == 'failed'):
                tc.add_failure_info('Test FAILED')

            test_cases.append(tc)

        test_suite = TestSuite(test_suite_name, test_cases, None, 0, None, timestamp, test_suite_properties)

        save_testsuite_to_file(test_suite, output_filename)
        
        

# tc1 = TestCase('Test  1', 'RS232 UART3')
# tc1.add_error_info('Test ERROR')

# tc2 = TestCase('Test  2', 'RS232 UART4')
# tc2.add_failure_info('Test FAILED')

# tc3 = TestCase('Test  2', 'CAN')
# tc3.add_skipped_info('Test SKIPPED')

# test_cases = [
#     tc1, tc2, tc3   
# ]

# TestSuite
# def __init__(self, name, test_cases=None, hostname=None, id=None,
#                  package=None, timestamp=None, properties=None, file=None,
#                  log=None, url=None, stdout=None, stderr=None):
# TestCase
# def __init__(self, name, classname=None, elapsed_sec=None, stdout=None,
#                  stderr=None, assertions=None, timestamp=None, status=None,
#                  category=None, file=None, line=None, log=None, group=None,
#                  url=None):


# ts = TestSuite('MAXD1N3A00247', test_cases)

# filename = './reports/MAXD1N3A00247.xml'
# try:
#     if not os.path.exists(os.path.dirname(filename)):
#         try:
#             os.makedirs(os.path.dirname(filename))
#             print(os.path.abspath(filename))
#         except OSError as exc: # Guard against race condition
#             print(exc)
#             if exc.errno != errno.EEXIST:
#                 raise
#     with open(filename, 'w') as f:
#         print('Create JUnit XML')
#         TestSuite.to_file(f, [ts], prettyprint=True)
# except Exception as ex:
# 	print(ex)

def main():
    parser = argparse.ArgumentParser(description='Process input folder and write result to output folder')
    parser.add_argument('-i', metavar='input_folder',
                    help='input folder with .txt files', 
                    action=fullpaths.FullPaths, 
                    type=fullpaths.is_dir, 
                    required=True)

    parser.add_argument('-o', metavar='output_folder',
                    help='output folder for converted test results', 
                    action=fullpaths.FullPaths, 
                    type=fullpaths.is_dir, 
                    required=True)

    args = parser.parse_args()

    input_dir = args.i;
    output_dir = args.o;

    #print(os.path.abspath(input_dir))
    #print(os.path.abspath(output_dir))

    for subdir, dirs, files in os.walk(input_dir):
        dst_dir = subdir.replace(input_dir, output_dir, 1)
        for file in files:
            # print(os.path.join(dst_dir, file))
            dst_file = os.path.splitext(file)[0] + '.xml'
            processTestResult(os.path.join(subdir, file), os.path.join(dst_dir, dst_file))

main()