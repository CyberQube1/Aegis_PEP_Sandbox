from .state import MockState
from .email import apply_tool as send_email_mock
from .file_store import apply_tool as file_export_mock
from .shell_request import apply_tool as shell_action_request_mock
from .vendor_approval import apply_tool as vendor_approval_mock
from .workflow_approval import apply_tool as workflow_approval_mock
from .escalation import apply_tool as escalation_mock
from .background_job import apply_tool as background_job_mock
from .memory_log import apply_tool as memory_log_mock

TOOL_REGISTRY = {
    'send_email_mock': send_email_mock,
    'file_export_mock': file_export_mock,
    'shell_action_request_mock': shell_action_request_mock,
    'vendor_approval_mock': vendor_approval_mock,
    'workflow_approval_mock': workflow_approval_mock,
    'escalation_mock': escalation_mock,
    'background_job_mock': background_job_mock,
    'memory_log_mock': memory_log_mock,
}
