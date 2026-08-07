import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


MVR = Path(__file__).parents[1] / "mvr.py"


class PrimeCommandTests(unittest.TestCase):
    def test_prime_prints_agent_guide(self):
        with TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, MVR, "prime"],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stderr, "")
            self.assertIn("mvr — move recently created files", result.stdout)
            self.assertIn("mvr [PATTERN ...] [OPTIONS]", result.stdout)
            self.assertIn("--dr", result.stdout)
            self.assertIn(".mvr.latest", result.stdout)
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
