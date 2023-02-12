import sys
import traceback
from os import getcwd, path
from time import sleep

import click
from rich import print
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from rift.cli.commands.utils import load_module
from rift.cli.config import ProjectConfig
from rift.cli.entry import entry
from rift.fift.test_result import TestError
from rift.fift.types import Cell
from rift.func.meta_contract import ContractMeta
from rift.runtime.config import FiftMode


class TestSession:
    target: str
    project: str
    tests: dict[str, dict[str, int]]
    progress_cache: dict[str, int]

    def cache_pg(self, k, p):
        self.progress_cache[k] = p

    def cached_progress(self, k):
        if k in self.progress_cache:
            return self.progress_cache[k]
        pg = self.progress()
        self.cache_pg(k, pg)
        return pg

    def progress(self):
        c = 0
        d = 0
        for _, tests in self.tests.items():
            for _, state in tests.items():
                c += 1
                if state != 0:
                    d += 1
        if c == 0:
            return 0
        return int((d * 100) / c)


def render_test_panel(session: TestSession) -> Panel:
    table = Table(show_header=False, expand=True, box=None)
    table.add_column("Test")
    table.add_column("Progress", justify="right")

    for test_tg, tests in session.tests.items():
        for (t, state) in tests.items():
            if state != 0:
                state_t = (
                    "[magenta] ✗[/magenta]"
                    if state == -1
                    else "[green] ✓[/green]"
                )
                state_t = Text.from_markup(state_t)
                progress = session.cached_progress(test_tg + "/" + t)
                t = Text.from_markup(
                    f"[white]{test_tg}[/white] -> [gray]{t}[/gray]",
                )
                t.append(state_t)
                pg_t = (
                    f"[magenta][{progress}%][/magenta]"
                    if state == -1
                    else f"[green][{progress}%][/green]"
                )
                pg_t = Text.from_markup(pg_t)
                table.add_row(t, pg_t)
    return Panel(
        table,
        title=f"Testing [yellow]{session.target}[/yellow] from [blue]{session.project}[/blue]",
    )


@entry.command(help="Tests an specific target")
@click.argument("target")
def test(target):
    FiftMode.activate()
    cwd = getcwd()
    config = ProjectConfig.working()
    if not config:
        click.echo(
            click.style("Not a rift project!", fg="red"),
        )
        return

    contracts_dir = path.join(cwd, "tests")
    build_dir = path.join(cwd, "build")
    
    if target == "all":
        targets = list(config.contracts.keys())
    else:
        targets = [target]

    for target in targets:
        contract_config = config.contracts[target]
        test_targets = contract_config.tests

        sys.path.append(cwd)
        session = TestSession()
        session.project = config.name
        session.target = target
        session.tests = {}
        session.progress_cache = {}

        with Live(render_test_panel(session), refresh_per_second=4) as live:
            for test_tg in test_targets:
                session.tests[test_tg] = {}
                fp = path.join(contracts_dir, test_tg + ".py")

                mod, *_ = load_module(fp, test_tg, patch=False)
                contracts = ContractMeta.defined_contracts()
                for contract in contracts:
                    contract_cfg = config.get_contract(contract.__name__)
                    name = contract_cfg.get_file_name()
                    boc_file = path.join(build_dir, f"{name}.patched.boc")
                    if not contract.__interface__:
                        if not path.exists(boc_file):
                            click.secho(
                                f"Couldn't find {name}.boc, Have you built the target? (rift build <target>)",
                                fg="red",
                            )
                            return
                        code_cell = Cell.load_from(boc_file)
                        contract.__code_cell__ = code_cell

                keys = list(filter(lambda x: x.startswith("test_"), mod.__dict__))
                for k in keys:
                    session.tests[test_tg][k] = False
                for k in keys:
                    try:
                        mod.__dict__[k]()
                        session.tests[test_tg][k] = 1
                    except TestError as te:
                        traceback.print_exception(te)
                        session.tests[test_tg][k] = -1
                    except Exception as e:
                        traceback.print_exception(e)
                        session.tests[test_tg][k] = -1
                    live.update(render_test_panel(session))
                    sleep(0.1)
