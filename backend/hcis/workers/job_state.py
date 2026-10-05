from hcis.core.enums import JobStatus

ALLOWED_TRANSITIONS = {
    JobStatus.QUEUED: {JobStatus.RUNNING, JobStatus.CANCELLED},
    JobStatus.RUNNING: {JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.DEGRADED,
                        JobStatus.CANCELLED, JobStatus.BLOCKED_EXTERNAL,
                        JobStatus.BLOCKED_PRIVACY_POLICY, JobStatus.BLOCKED_BUDGET_POLICY},
    JobStatus.DEGRADED: {JobStatus.RUNNING, JobStatus.FAILED, JobStatus.SUCCEEDED},
    JobStatus.FAILED: {JobStatus.QUEUED},
    JobStatus.BLOCKED_EXTERNAL: {JobStatus.QUEUED},
    JobStatus.BLOCKED_PRIVACY_POLICY: {JobStatus.QUEUED},
    JobStatus.BLOCKED_BUDGET_POLICY: {JobStatus.QUEUED},
    JobStatus.SUCCEEDED: set(),
    JobStatus.CANCELLED: set(),
}

def assert_transition(current: JobStatus, target: JobStatus) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"illegal job transition: {current} -> {target}")
