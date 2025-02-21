"""Test the parallel portfolio CLI entry point."""
from pathlib import Path
import pytest
import shutil

from sparkle.CLI import run_parallel_portfolio, add_solver, add_instances

from tests.CLI import tools as cli_tools


@pytest.mark.integration
def test_parallel_portfolio_command(tmp_path: Path,
                                    monkeypatch: pytest.MonkeyPatch) -> None:
    """Test for CLI entry point parallel_portfolio."""
    # NOTE: This test is disabled because it is unreliable as the command awaits
    # Slurm jobs to finish before returning, therefore its disabled
    return
    solver_pbo = Path("Examples/Resources/Solvers/PbO-CCSAT-Generic").absolute()
    solver_csccsat = Path("Examples/Resources/Solvers/CSCCSat").absolute()
    solver_minisat = Path("Examples/Resources/Solvers/MiniSAT").absolute()
    single_instance_ptn = Path("Examples/Resources/Instances/PTN/bce7824.cnf").absolute()
    settings_path = cli_tools.get_settings_path()
    monkeypatch.chdir(tmp_path)  # Execute in PyTest tmp dir
    # Create single instance data set for speed up
    tmp_ptn = Path("PTN")
    tmp_ptn.mkdir()
    shutil.copy(single_instance_ptn, tmp_ptn)

    # Setup platform
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_solver.main([str(solver_pbo)])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 0

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_solver.main([str(solver_csccsat)])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 0

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_solver.main([str(solver_minisat)])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 0

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_instances.main([str(tmp_ptn)])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 0

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run_parallel_portfolio.main(["--instance-path", tmp_ptn.name,
                                     "--settings-file", str(settings_path)])
    assert pytest_wrapped_e.type is SystemExit
    assert pytest_wrapped_e.value.code == 0
