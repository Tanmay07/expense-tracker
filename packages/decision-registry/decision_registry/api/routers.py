from fastapi import APIRouter, Depends, HTTPException
from typing import List

from .dependencies import get_sdk
from ..application.sdk import DecisionSDK
from ..domain.models import Decision, DecisionRelationship

router = APIRouter()


@router.post("/decisions", response_model=Decision)
def create_decision(decision: Decision, sdk: DecisionSDK = Depends(get_sdk)):
    return sdk.create_decision(decision)


@router.get("/decisions/{decision_id}", response_model=Decision)
def get_decision(decision_id: str, sdk: DecisionSDK = Depends(get_sdk)):
    decision = sdk.get_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.delete("/decisions/{decision_id}/archive", response_model=Decision)
def archive_decision(decision_id: str, sdk: DecisionSDK = Depends(get_sdk)):
    decision = sdk.archive_decision(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    return decision


@router.post(
    "/decisions/{decision_id}/relationships", response_model=DecisionRelationship
)
def add_relationship(
    decision_id: str,
    relationship: DecisionRelationship,
    sdk: DecisionSDK = Depends(get_sdk),
):
    if relationship.source_decision_id != decision_id:
        raise HTTPException(status_code=400, detail="Decision ID mismatch")
    return sdk.add_relationship(relationship)


@router.get(
    "/decisions/{decision_id}/relationships", response_model=List[DecisionRelationship]
)
def get_relationships(decision_id: str, sdk: DecisionSDK = Depends(get_sdk)):
    return sdk.get_relationships(decision_id)
