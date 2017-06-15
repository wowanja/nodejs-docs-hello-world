from junit_xml import TestSuite, TestCase

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
try:
	with open('reports/MAXD1N3A00247.xml', 'w') as f:
		TestSuite.to_file(f, [ts], prettyprint=True)
except Exception as ex:
	print ex
	