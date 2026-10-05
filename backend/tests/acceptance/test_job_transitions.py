import pytest
from hcis.workers.job_state import assert_transition
from hcis.core.enums import JobStatus
def test_terminal_success_cannot_return_running():
    with pytest.raises(ValueError):
        assert_transition(JobStatus.SUCCEEDED,JobStatus.RUNNING)
