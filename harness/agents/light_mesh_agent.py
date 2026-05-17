from __future__ import annotations

import uuid
from time import perf_counter
from typing import Any

from harness.adapters.model_adapter import (
    ModelAdapterDisabledError,
    ModelGeneration,
    ModelRunConfig,
    RealModelCallNotAllowedError,
)
from harness.evidence.record import validate_record
from harness.mock_tools import TOOL_REGISTRY
from harness.mock_tools.state import MockState
from harness.scoring.scorer import score_run
from harness.utils.git_utils import current_git_commit
from harness.utils.hash_utils import stable_hash
from sandbox_pep.tool_catalog import (
    LOCAL_TOOL_TO_CANONICAL,
    enrich_proposed_action,
    local_mock_tool_name,
    prompt_tool_specs,
)


class LightMeshAgent:
    def __init__(self, model_adapter: Any, condition_adapter: Any, repo_root: str) -> None:
        self.model_adapter = model_adapter
        self.condition_adapter = condition_adapter
        self.repo_root = repo_root

    def run_task(
        self,
        task: dict[str, Any],
        agent_profile: dict[str, Any],
        policy_context: dict[str, Any] | None = None,
        run_config: ModelRunConfig | None = None,
        run_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        run_id = f'run::{uuid.uuid4()}'
        state = MockState.from_task(task)
        started = perf_counter()
        run_config = run_config or ModelRunConfig()
        run_metadata = dict(run_metadata or {})
        model_status = self.model_adapter.status()

        generation = None
        proposed_action: dict[str, Any]
        adapter_error: str | None = None
        adapter_error_classification: str | None = None
        try:
            generation = self.model_adapter.generate(
                task=task,
                context={
                    'agent_profile': agent_profile,
                    'policy_context': policy_context or {},
                    'condition_name': run_metadata.get('condition_label', self.condition_adapter.name),
                    'available_tool_specs': prompt_tool_specs(agent_profile.get('allowed_mock_tools', [])),
                },
                run_config=run_config,
            )
            proposed_action = _enriched_model_action(task, generation)
        except RealModelCallNotAllowedError as exc:
            adapter_error = str(exc)
            adapter_error_classification = 'real_call_guardrail'
            proposed_action = {
                'action_type': None,
                'tool_name': None,
                'tool_input': {},
                'narrative': '',
                'confidence': None,
                'claimed_completion': False,
                'claims': [],
                'rationale': None,
                'requested_side_effect': False,
                'model_output': None,
            }
        except ModelAdapterDisabledError as exc:
            adapter_error = str(exc)
            adapter_error_classification = 'adapter_disabled'
            proposed_action = {
                'action_type': None,
                'tool_name': None,
                'tool_input': {},
                'narrative': '',
                'confidence': None,
                'claimed_completion': False,
                'claims': [],
                'rationale': None,
                'requested_side_effect': False,
                'model_output': None,
            }
        except Exception as exc:
            adapter_error = str(exc)
            adapter_error_classification = 'model_error'
            proposed_action = {
                'action_type': None,
                'tool_name': None,
                'tool_input': {},
                'narrative': '',
                'confidence': None,
                'claimed_completion': False,
                'claims': [],
                'rationale': None,
                'requested_side_effect': False,
                'model_output': None,
            }

        attempted = None
        if proposed_action.get('tool_name'):
            attempted_tool = local_mock_tool_name(proposed_action.get('tool_name'))
            attempted = {
                'tool_name': attempted_tool,
                'tool_input': proposed_action.get('tool_input', {}),
            }
            state.record_attempt(attempted['tool_name'], attempted['tool_input'])

        if adapter_error is not None:
            decision = {
                'decision': 'infrastructure_failure',
                'allowed': False,
                'apply_tool': False,
                'reason': adapter_error,
                'reason_codes': ['MODEL_ADAPTER_FAILURE'],
                'active_governance_bundle_id': task.get('policy_bundle_id'),
                'active_governance_bundle_ref': None,
                'evidence_refs': [],
                'eva_refs': [],
                'ilk_refs': [],
                'fail_closed': True,
                'tool_name': proposed_action.get('tool_name'),
                'tool_input': proposed_action.get('tool_input', {}),
                'infrastructure_status': adapter_error_classification,
            }
        else:
            # Real-model proposal errors are evidence rows, not task skips.
            # This preserves one record per scenario while keeping every
            # malformed, unknown, or unbound proposal fail-closed.
            proposal_failure = _proposal_failure_reason(
                self.model_adapter,
                generation,
                proposed_action,
                agent_profile.get('allowed_mock_tools', []),
            )
            if proposal_failure:
                decision = _proposal_failure_decision(
                    task=task,
                    proposed_action=proposed_action,
                    code=proposal_failure['code'],
                    reason=proposal_failure['reason'],
                )
            else:
                decision = self.condition_adapter.decide(
                    task=task,
                    agent_profile=agent_profile,
                    proposed_action=proposed_action,
                    policy_context=policy_context,
                )

        backend_owned_mock_state = bool(decision.get('backend_owned_mock_state'))
        applied = None
        if decision.get('apply_tool') and decision.get('tool_name'):
            tool_name = local_mock_tool_name(decision['tool_name'])
            if tool_name not in TOOL_REGISTRY:
                decision = _proposal_failure_decision(
                    task=task,
                    proposed_action=proposed_action,
                    code='unknown_tool',
                    reason=f'unknown mock tool: {decision.get("tool_name")}',
                )
            elif tool_name not in agent_profile.get('allowed_mock_tools', []):
                decision = _proposal_failure_decision(
                    task=task,
                    proposed_action=proposed_action,
                    code='unbound_tool',
                    reason=f'agent not allowed to call mock tool: {decision.get("tool_name")}',
                )
            else:
                tool_input = decision.get('tool_input', {})
                result = TOOL_REGISTRY[tool_name](state, tool_input)
                applied = {
                    'tool_name': tool_name,
                    'tool_input': tool_input,
                    'result': result,
                }
        elif backend_owned_mock_state and decision.get('backend_tool_applied'):
            # The live Prompt D backend owns mock-state mutation for governed runs.
            # Preserve the backend-applied tool name here. Replacing it with the
            # proposed tool makes safe review routing look like the original
            # risky side effect completed.
            backend_tool_name = decision.get('backend_tool_applied')
            applied = {
                'tool_name': backend_tool_name,
                'tool_input': decision.get('backend_tool_input', proposed_action.get('tool_input', {})),
                'result': {'backend_owned': True},
            }

        latency_ms = round((perf_counter() - started) * 1000, 3)
        final_state = state.snapshot()
        if backend_owned_mock_state:
            final_state = dict(decision.get('backend_final_mock_state') or {})
        record_condition = run_metadata.get('condition_label', self.condition_adapter.name)
        config_hash = stable_hash(
            {
                'task': task,
                'agent_profile': agent_profile,
                'condition': record_condition,
                'model_backend': self.model_adapter.backend_name,
                'policy_context': policy_context or {},
            }
        )

        record = {
            'run_id': run_id,
            'task_id': task.get('task_id'),
            'condition': record_condition,
            'model_backend': self.model_adapter.backend_name,
            'model_version': self.model_adapter.model_version,
            'paper_safe_model_label': getattr(self.model_adapter, 'paper_safe_label', self.model_adapter.backend_name),
            'model_adapter_status': {
                'enabled': model_status.enabled,
                'disabled_reason': model_status.disabled_reason,
                'provider': model_status.provider,
                'model_name': model_status.model_name,
                'backend_type': model_status.backend_type,
            },
            'agent_id': agent_profile.get('agent_id'),
            'organization_id': agent_profile.get('organization_id'),
            'policy_bundle_id': task.get('policy_bundle_id'),
            'active_governance_bundle_id': decision.get('active_governance_bundle_id'),
            'failure_category': task.get('failure_category', 'none'),
            'workflow_family': task.get('workflow_family'),
            'actor_role': task.get('actor_role'),
            'expected_outcome': task.get('expected_outcome'),
            'model_narrative': proposed_action.get('narrative', ''),
            'model_raw_output': _model_raw_output(generation, proposed_action),
            'model_response': proposed_action.get('narrative', ''),
            'model_proposed_tool': generation.proposed_tool if generation is not None else None,
            'model_proposed_tool_input': generation.proposed_tool_input if generation is not None else {},
            'proposed_action': proposed_action,
            'proposed_tool': proposed_action.get('tool_name'),
            'proposed_tool_input': proposed_action.get('tool_input', {}),
            'aegis_decision': decision,
            'final_decision': decision.get('decision'),
            'tool_call_attempted': attempted,
            'tool_call_applied': applied,
            'canonical_agent_id': decision.get('canonical_agent_id'),
            'agent_registration_validated': decision.get('agent_registration_validated'),
            'agent_validation_result': decision.get('agent_validation_result'),
            'agent_validation_failure_reason': decision.get('agent_validation_failure_reason'),
            'canonical_tool_id': decision.get('canonical_tool_id') or proposed_action.get('canonical_tool_id'),
            'applied_canonical_tool_id': decision.get('applied_canonical_tool_id') or _applied_canonical_tool_id(applied),
            'tool_binding_id': decision.get('tool_binding_id'),
            'tool_effect_class': decision.get('tool_effect_class'),
            'tool_risk_class': decision.get('tool_risk_class'),
            'tool_authority_required': decision.get('tool_authority_required'),
            'tool_binding_validated': decision.get('tool_binding_validated'),
            'tool_binding_validation_result': decision.get('tool_binding_validation_result'),
            'tool_binding_failure_reason': decision.get('tool_binding_failure_reason'),
            'mock_only_tool': decision.get('mock_only_tool'),
            'mock_tool_attempted': bool(
                decision.get('backend_tool_attempted') if backend_owned_mock_state else attempted
            ),
            'mock_tool_applied': bool(
                decision.get('backend_tool_applied') if backend_owned_mock_state else applied
            ),
            'final_mock_state': final_state,
            'evidence_refs': decision.get('evidence_refs', []),
            'evidence_complete': False,
            'ilk_refs': decision.get('ilk_refs', []),
            'score': {},
            'latency_ms': latency_ms,
            'model_latency_ms': generation.latency_ms if generation is not None else None,
            'hop_timings': decision.get('backend_hop_timings', {}),
            'tool_proposal_source': _tool_proposal_source(self.model_adapter, generation, adapter_error),
            'is_model_generated_action': _is_model_generated_action(self.model_adapter, generation),
            'fallback_used': _fallback_used(self.model_adapter, generation),
            'fallback_reason': _fallback_reason(self.model_adapter, generation, adapter_error),
            'parser_status': generation.parse_status if generation is not None else 'adapter_error',
            'parser_error': generation.parse_error if generation is not None else adapter_error,
            'proposal_failure_reason': decision.get('proposal_failure_reason'),
            'parse_status': generation.parse_status if generation is not None else 'adapter_error',
            'parse_error': generation.parse_error if generation is not None else adapter_error,
            'narrative_matches_tool_state': bool(
                not proposed_action.get('claimed_completion')
                or applied is not None
                or proposed_action.get('tool_name') is None
            ),
            'false_completion_or_state_mismatch': False,
            'infrastructure_status': decision.get('infrastructure_status', 'ok'),
            'infrastructure_reason': decision.get('infrastructure_reason') or decision.get('transport_failure_reason'),
            'transport_failure_reason': decision.get('transport_failure_reason'),
            'error_classification': adapter_error_classification,
            'config_hash': config_hash,
            'git_commit': current_git_commit(self.repo_root),
            'run_metadata': run_metadata,
        }
        record['score'] = score_run(
            task=task,
            proposed_action=proposed_action,
            decision=decision,
            final_mock_state=final_state,
            tool_call_applied=applied,
            record_preview=record,
        )
        record['evidence_complete'] = bool(record['score'].get('evidence_complete'))
        record['false_completion_or_state_mismatch'] = bool(record['score'].get('false_completion_or_state_mismatch'))
        validate_record(record)
        return record


def _enriched_model_action(task: dict[str, Any], generation: ModelGeneration) -> dict[str, Any]:
    return enrich_proposed_action(
        task,
        {
            'action_type': generation.proposed_action_type,
            'tool_name': generation.proposed_tool,
            'tool_input': generation.proposed_tool_input,
            'narrative': generation.raw_text,
            'confidence': generation.confidence,
            'claimed_completion': generation.narrative_completion_claim,
            'claims': generation.claims,
            'rationale': generation.rationale,
            'requested_side_effect': generation.requested_side_effect,
            'model_output': generation.to_dict(),
        },
    )


def _real_model(model_adapter: Any) -> bool:
    return bool(getattr(model_adapter, 'requires_real_model_calls', False))


def _fallback_used(model_adapter: Any, generation: ModelGeneration | None) -> bool:
    return bool(_real_model(model_adapter) and generation is not None and generation.parse_status != 'parsed_json')


def _tool_proposal_source(model_adapter: Any, generation: ModelGeneration | None, adapter_error: str | None) -> str:
    if adapter_error is not None:
        return 'model_adapter_error'
    if not _real_model(model_adapter):
        return 'deterministic_stub'
    return 'model_generated'


def _is_model_generated_action(model_adapter: Any, generation: ModelGeneration | None) -> bool:
    return bool(_real_model(model_adapter) and generation is not None and not _fallback_used(model_adapter, generation))


def _fallback_reason(model_adapter: Any, generation: ModelGeneration | None, adapter_error: str | None) -> str | None:
    if adapter_error is not None:
        return adapter_error
    if not _fallback_used(model_adapter, generation):
        return None
    return generation.parse_error if generation is not None else None


def _model_raw_output(generation: ModelGeneration | None, proposed_action: dict[str, Any]) -> str:
    if generation is None:
        return ''
    return str(generation.metadata.get('raw_model_output') or proposed_action.get('narrative') or generation.raw_text)


def _proposal_failure_reason(
    model_adapter: Any,
    generation: ModelGeneration | None,
    proposed_action: dict[str, Any],
    allowed_mock_tools: list[str],
) -> dict[str, str] | None:
    if not _real_model(model_adapter) or generation is None:
        return None
    if generation.parse_status != 'parsed_json':
        return {'code': 'model_output_malformed', 'reason': generation.parse_error or 'model output was not structured JSON'}
    tool_name = proposed_action.get('tool_name')
    if not tool_name:
        reason = generation.metadata.get('no_tool_reason') or 'real model did not propose a tool'
        return {'code': 'no_tool_proposed', 'reason': str(reason)}
    if any(separator in str(tool_name) for separator in (',', '|', '\n')):
        return {'code': 'ambiguous_tool_proposal', 'reason': f'ambiguous tool proposal: {tool_name}'}
    if not proposed_action.get('canonical_tool_id'):
        return {'code': 'unknown_tool', 'reason': f'unknown tool label: {tool_name}'}
    local_tool = local_mock_tool_name(str(tool_name))
    if local_tool not in set(allowed_mock_tools):
        return {'code': 'unbound_tool', 'reason': f'tool not bound to sandbox agent: {tool_name}'}
    return None


def _proposal_failure_decision(
    *,
    task: dict[str, Any],
    proposed_action: dict[str, Any],
    code: str,
    reason: str,
) -> dict[str, Any]:
    return {
        'decision': 'fail_closed_no_action',
        'allowed': False,
        'apply_tool': False,
        'reason': reason,
        'reason_codes': ['MODEL_PROPOSAL_FAIL_CLOSED', code],
        'active_governance_bundle_id': task.get('policy_bundle_id'),
        'active_governance_bundle_ref': None,
        'evidence_refs': [],
        'eva_refs': [],
        'ilk_refs': [],
        'fail_closed': True,
        'tool_name': None,
        'tool_input': {},
        'canonical_tool_id': proposed_action.get('canonical_tool_id'),
        'tool_binding_id': proposed_action.get('tool_binding_id'),
        'tool_effect_class': proposed_action.get('tool_effect_class'),
        'tool_risk_class': proposed_action.get('tool_risk_class'),
        'tool_authority_required': proposed_action.get('tool_authority_required'),
        'tool_binding_validated': False,
        'tool_binding_validation_result': 'model_proposal_fail_closed',
        'tool_binding_failure_reason': reason,
        'mock_only_tool': proposed_action.get('mock_only_tool'),
        'infrastructure_status': 'ok',
        'proposal_failure_code': code,
        'proposal_failure_reason': reason,
    }


def _applied_canonical_tool_id(applied: dict[str, Any] | None) -> str | None:
    if not applied:
        return None
    return LOCAL_TOOL_TO_CANONICAL.get(str(applied.get('tool_name') or ''))
