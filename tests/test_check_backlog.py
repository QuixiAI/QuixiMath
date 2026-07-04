import os
import sys
import unittest

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tools.check_backlog import scan


class TestCheckBacklog(unittest.TestCase):
    def test_flags_registered_contract_name(self):
        todo = "- [ ] Some item · `FooGenerator` · middle · d3"
        self.assertEqual(scan(todo, {"FooGenerator"}),
                         ["FooGenerator"])

    def test_ignores_unregistered_and_checked_lines(self):
        todo = ("- [ ] Some item · `FooGenerator` · middle · d3\n"
                "- [x] Done item · `BarGenerator` · middle · d3\n")
        self.assertEqual(scan(todo, {"BarGenerator"}), [])

    def test_ignores_mid_line_mentions(self):
        # A registered class referenced in prose (not the contract
        # position) must not be flagged.
        todo = ("- [ ] RK steps (extends `EulerMethodGenerator`) · "
                "`RungeKuttaGenerator` · college · d4")
        self.assertEqual(scan(todo, {"EulerMethodGenerator"}), [])
        self.assertEqual(scan(todo, {"RungeKuttaGenerator"}),
                         ["RungeKuttaGenerator"])

    def test_current_backlog_is_clean(self):
        from dolphin_math_datagen import ALL_GENERATORS
        registered = {type(g).__name__ for g in ALL_GENERATORS}
        with open(os.path.join(repo_root, "TODO.md"),
                  encoding="utf-8") as fh:
            todo = fh.read()
        self.assertEqual(scan(todo, registered), [])


if __name__ == "__main__":
    unittest.main()
