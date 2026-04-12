from django.db import transaction
from django.utils import timezone

from apps.tasks.models import Task
from apps.notifications.models import Notification
from apps.workflows.models import (
    Workflow,
    WorkflowStatus,
    WorkflowConditionOperator,
    WorkflowActionType,
)
from .models import WorkflowRun, ActionLog, RunStatus, ActionLogStatus
from apps.accounts.models import User
from django.core.mail import send_mail
from django.conf import settings



def emit_event(trigger_type, lead, context=None):
    """
    Entry point for the automation engine.
    Finds active workflows matching the trigger and executes them.
    """
    if context is None:
        context = {}

    workflows = (
        Workflow.objects
        .filter(trigger_type=trigger_type, status=WorkflowStatus.ACTIVE)
        .prefetch_related("conditions", "actions")
    )

    runs = []

    for workflow in workflows:
        if conditions_match(workflow, lead, context):
            run = execute_workflow(workflow=workflow, lead=lead, trigger_type=trigger_type, context=context)
            runs.append(run)

    return runs


def conditions_match(workflow, lead, context=None):
    """
    Returns True if all workflow conditions match the lead/context.
    If no conditions exist, returns True.
    """
    conditions = workflow.conditions.all()

    if not conditions:
        return True

    for condition in conditions:
        actual_value = get_field_value(lead, context or {}, condition.field_name)

        if not evaluate_condition(
            actual_value=actual_value,
            operator=condition.operator,
            expected_value=condition.field_value,
        ):
            return False

    return True


def get_field_value(lead, context, field_name):
    """
    Supports lead field lookup first, then context lookup.
    """
    if hasattr(lead, field_name):
        value = getattr(lead, field_name)
        if value is None:
            return None
        return str(value)

    if field_name in context:
        value = context[field_name]
        if value is None:
            return None
        return str(value)

    return None

def evaluate_condition(actual_value, operator, expected_value):
    actual_value = "" if actual_value is None else str(actual_value)
    expected_value = "" if expected_value is None else str(expected_value)

    if operator == WorkflowConditionOperator.EQUALS:
        return actual_value == expected_value

    if operator == WorkflowConditionOperator.NOT_EQUALS:
        return actual_value != expected_value

    return False


@transaction.atomic
def execute_workflow(workflow, lead, trigger_type, context=None):
    """
    Executes a single workflow for a lead.
    """
    if context is None:
        context = {}

    workflow_run = WorkflowRun.objects.create(
        workflow=workflow,
        lead=lead,
        trigger_type=trigger_type,
        status=RunStatus.RUNNING,
    )

    actions = workflow.actions.filter(is_active=True).order_by("action_order")

    success_count = 0
    failure_count = 0
    last_error = None

    for action in actions:
        log = ActionLog.objects.create(
            workflow_run=workflow_run,
            workflow_action=action,
            status=ActionLogStatus.PENDING,
        )

        try:
            message = execute_action(action=action, lead=lead, context=context)

            log.status = ActionLogStatus.SUCCESS
            log.message = message
            log.executed_at = timezone.now()
            log.save(update_fields=["status", "message", "executed_at"])

            success_count += 1

        except Exception as exc:
            log.status = ActionLogStatus.FAILED
            log.error_message = str(exc)
            log.executed_at = timezone.now()
            log.save(update_fields=["status", "error_message", "executed_at"])

            failure_count += 1
            last_error = str(exc)

    workflow_run.finished_at = timezone.now()

    if failure_count == 0:
        workflow_run.status = RunStatus.SUCCESS
        workflow_run.error_message = None
    elif success_count == 0:
        workflow_run.status = RunStatus.FAILED
        workflow_run.error_message = last_error
    else:
        workflow_run.status = RunStatus.PARTIAL_SUCCESS
        workflow_run.error_message = last_error

    workflow_run.save(update_fields=["status", "finished_at", "error_message"])

    return workflow_run


def execute_action(action, lead, context=None):
    """
    Dispatches a workflow action to the correct handler.
    """
    if context is None:
        context = {}

    if action.action_type == WorkflowActionType.ASSIGN_AGENT:
        return execute_assign_agent(action.config, lead)

    if action.action_type == WorkflowActionType.CREATE_TASK:
        return execute_create_task(action.config, lead)

    if action.action_type == WorkflowActionType.SEND_NOTIFICATION:
        return execute_send_notification(action.config, lead)

    if action.action_type == WorkflowActionType.SEND_EMAIL:
        return execute_send_email(action.config, lead)

    raise ValueError(f"Unsupported action type: {action.action_type}")


def execute_assign_agent(config, lead):
    assignment_type = config.get("assignment_type")

    if assignment_type != "specific":
        raise ValueError("Only 'specific' assignment_type is supported in MVP.")

    agent_id = config.get("agent_id")
    if not agent_id:
        raise ValueError("agent_id is required for assign_agent action.")

    try:
        agent = User.objects.get(id=agent_id, role="agent", is_active=True)
    except User.DoesNotExist:
        raise ValueError("Configured agent not found or inactive.")

    lead.assigned_agent = agent
    lead.save(update_fields=["assigned_agent", "updated_at"])

    return f"Lead assigned to agent {agent.full_name} (id={agent.id})."


def execute_create_task(config, lead):
    title = config.get("title_template")
    description = config.get("description", "")
    due_in_days = config.get("due_in_days")
    assign_to = config.get("assign_to")

    if not title:
        raise ValueError("title_template is required for create_task action.")

    assigned_user = None

    if assign_to == "assigned_agent":
        assigned_user = lead.assigned_agent
        if not assigned_user:
            raise ValueError("Lead has no assigned agent for task assignment.")

    due_date = None
    if due_in_days is not None:
        due_date = timezone.now() + timezone.timedelta(days=int(due_in_days))

    task = Task.objects.create(
        lead=lead,
        assigned_to=assigned_user,
        title=title,
        description=description,
        due_date=due_date,
        created_by_user=lead.created_by,
    )

    return f"Task created successfully (id={task.id})."

def execute_send_notification(config, lead):
    target = config.get("target")
    title = config.get("title")
    message_template = config.get("message_template")

    if target != "assigned_agent":
        raise ValueError("Only 'assigned_agent' target is supported in MVP.")

    if not lead.assigned_agent:
        raise ValueError("Lead has no assigned agent to notify.")

    if not title:
        raise ValueError("title is required for send_notification action.")

    if not message_template:
        raise ValueError("message_template is required for send_notification action.")

    message = render_template(message_template, lead)

    notification = Notification.objects.create(
        user=lead.assigned_agent,
        lead=lead,
        type="info",
        title=title,
        message=message,
    )

    return f"Notification created successfully (id={notification.id})."

def execute_send_email(config, lead):
    target = config.get("target")
    subject = config.get("subject")
    body_template = config.get("body_template")

    if target != "lead":
        raise ValueError("Only 'lead' target is supported in MVP.")

    if not lead.email:
        raise ValueError("Lead does not have an email address.")

    if not subject:
        raise ValueError("subject is required for send_email action.")

    if not body_template:
        raise ValueError("body_template is required for send_email action.")

    body = render_template(body_template, lead)

    send_mail(
        subject=subject,
        message=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=[lead.email],
        fail_silently=False,
    )

    return f"Email sent successfully to {lead.email}."

def render_template(template_string, lead):
    """
    Very simple template rendering for MVP.
    """
    return (
        template_string
        .replace("{{lead.full_name}}", lead.full_name or "")
        .replace("{{lead.email}}", lead.email or "")
        .replace("{{lead.company_name}}", lead.company_name or "")
        .replace("{{lead.status}}", lead.status or "")
    )