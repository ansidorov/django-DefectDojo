import datetime
from django.test import TestCase

from dojo.models import Test, Finding
from dojo.tools.cyclonedx.parser import CycloneDXParser


class TestParser(TestCase):

    def test_grype_report(self):
        with open("dojo/unittests/scans/cyclonedx/grype_dd_1_14_1.xml") as file:
            parser = CycloneDXParser()
            findings = list(parser.get_findings(file, Test()))
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(619, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("Deprecated", finding.component_name)
                self.assertEqual("1.2.12", finding.component_version)
                self.assertEqual(datetime.date(2021, 4, 13), datetime.datetime.date(finding.date))
            with self.subTest(i=200):
                finding = findings[200]
                self.assertEqual("High", finding.severity)
                self.assertEqual("jira", finding.component_name)
                self.assertEqual("2.0.0", finding.component_version)
                self.assertEqual("CVE-2019-8443", finding.cve)
                self.assertEqual(datetime.date(2021, 4, 13), datetime.datetime.date(finding.date))

    def test_spec1_report(self):
        """Test a report from the spec itself"""
        with open("dojo/unittests/scans/cyclonedx/spec1.xml") as file:
            parser = CycloneDXParser()
            findings = list(parser.get_findings(file, Test()))
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(2, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertIsNone(finding.cve)
                self.assertEqual("Info", finding.severity)
            with self.subTest(i=1):
                finding = findings[1]
                self.assertEqual("CVE-2018-7489", finding.cve)
                self.assertEqual("Critical", finding.severity)
                self.assertIn(finding.cwe, [184, 502])  # there is 2 CWE in the report
                self.assertEqual("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", finding.cvssv3)
                self.assertEqual(9.8, finding.cvssv3_score)
                self.assertEqual("jackson-databind", finding.component_name)
                self.assertEqual("2.9.9", finding.component_version)
                self.assertEqual("CVE-2018-7489", finding.unique_id_from_tool)

    def test_cyclonedx_bom_report(self):
        with open("dojo/unittests/scans/cyclonedx/cyclonedx_bom.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(73, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("asteval", finding.component_name)
                self.assertEqual("0.9.23", finding.component_version)

    def test_cyclonedx_jake_report(self):
        """Test a report generated by Jake"""
        with open("dojo/unittests/scans/cyclonedx/jake.xml") as file:
            parser = CycloneDXParser()
            findings = parser.get_findings(file, Test())
            for finding in findings:
                self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertEqual(204, len(findings))
            with self.subTest(i=0):
                finding = findings[0]
                self.assertEqual("Info", finding.severity)
                self.assertEqual("yaspin", finding.component_name)
                self.assertEqual("0.16.0", finding.component_version)
