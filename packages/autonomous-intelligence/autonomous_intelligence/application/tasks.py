import logging
from autonomous_intelligence.application.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def mission_planner_task(agent_id: str, mission_id: str):
    logger.info(f"Running mission planner for agent {agent_id}, mission {mission_id}")
    return {"status": "success", "agent_id": agent_id}


@celery_app.task
def goal_monitor_task(agent_id: str):
    logger.info(f"Running goal monitor for agent {agent_id}")
    return {"status": "success", "agent_id": agent_id}


@celery_app.task
def agent_scheduler_task():
    logger.info("Running agent scheduler")
    return {"status": "success"}


@celery_app.task
def evaluation_worker_task(agent_id: str):
    logger.info(f"Running evaluation worker for agent {agent_id}")
    return {"status": "success", "agent_id": agent_id}


@celery_app.task
def planning_worker_task(agent_id: str):
    logger.info(f"Running planning worker for agent {agent_id}")
    return {"status": "success", "agent_id": agent_id}


@celery_app.task
def memory_maintenance_task():
    logger.info("Running memory maintenance")
    return {"status": "success"}


@celery_app.task
def consensus_worker_task(agent_ids: list):
    logger.info(f"Running consensus worker for agents {agent_ids}")
    return {"status": "success"}
