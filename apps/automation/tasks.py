import logging
from celery import shared_task
from apps.leads.models import Lead
from .services import emit_event

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def run_workflow_event(self, trigger_type, lead_id, context=None):
    logger.info("run_workflow_event started | trigger=%s | lead_id=%s", trigger_type, lead_id)

    lead = Lead.objects.get(id=lead_id)
    logger.info("Lead fetched successfully | id=%s | name=%s", lead.id, lead.full_name)

    result = emit_event(trigger_type=trigger_type, lead=lead, context=context or {})
    logger.info("emit_event completed | runs=%s", len(result))

    return {"workflow_runs_created": len(result)}