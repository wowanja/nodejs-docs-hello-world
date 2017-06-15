import os
from junit_xml import TestSuite, TestCase

print('In Python Script')
tc1 = TestCase('Test  1', 'RS232 UART3')
tc1.add_error_info('Test ERROR')

tc2 = TestCase('Test  2', 'RS232 UART4')
tc2.add_failure_info('Test FAILED')

tc3 = TestCase('Test  2', 'CAN')
tc3.add_skipped_info('Test SKIPPED')

test_cases = [
    tc1, tc2, tc3   
]
ts = TestSuite('MAXD1N3A00247', test_cases)

filename = './reports/MAXD1N3A00247.xml'
try:
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
            print(os.path.abspath(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as f:
        print('Create JUnit XML')
        TestSuite.to_file(f, [ts], prettyprint=True)
except Exception as ex:
	print(ex)