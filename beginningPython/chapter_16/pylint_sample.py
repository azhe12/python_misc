#!/usr/bin/python
import subprocess, unittest

class PylintTestCase(unittest.TestCase):
    def testPylint(self):
        cmd = 'pylint', '-rn', 'DocTestSample.py'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        self.assertEqual(p.stdout.read(), '')

if __name__ == '__main__':unittest.main()
