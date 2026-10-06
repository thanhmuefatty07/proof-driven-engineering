import argparse
import runpy
import unittest
from pathlib import Path


EMPTY = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def contract_suite(fingerprints):
    class FingerprintContractTests(unittest.TestCase):
        def test_known_sha256_vectors(self):
            self.assertEqual(fingerprints([b"", b"abc"]), [EMPTY, ABC])

        def test_order_and_duplicates(self):
            self.assertEqual(fingerprints([b"abc", b"", b"abc"]), [ABC, EMPTY, ABC])

        def test_single_pass_iterable(self):
            source = iter([b"abc", b""])
            self.assertEqual(fingerprints(source), [ABC, EMPTY])
            with self.assertRaises(StopIteration):
                next(source)

        def test_caller_data_is_preserved(self):
            source = [b"abc", b""]
            before = source.copy()
            self.assertEqual(fingerprints(source), [ABC, EMPTY])
            self.assertEqual(source, before)
            self.assertEqual(fingerprints([]), [])

        def test_non_bytes_entries_are_rejected(self):
            for invalid in ("abc", 123, None, bytearray(b"abc"), memoryview(b"abc")):
                with self.subTest(invalid_type=type(invalid).__name__):
                    with self.assertRaises(TypeError):
                        fingerprints([b"abc", invalid])

    return unittest.defaultTestLoader.loadTestsFromTestCase(FingerprintContractTests)


def main():
    parser = argparse.ArgumentParser(description="Run digest contract checks on a reviewed isolated candidate.")
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    candidate = args.candidate.resolve(strict=True)
    namespace = runpy.run_path(str(candidate))
    result = unittest.TextTestRunner(verbosity=2).run(contract_suite(namespace["fingerprints"]))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
