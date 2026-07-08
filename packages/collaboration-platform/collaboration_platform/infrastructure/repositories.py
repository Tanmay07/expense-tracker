from typing import List, Optional, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import (
    Base,
    HouseholdModel,
    HouseholdMemberModel,
    DelegationModel,
    AdvisorModel,
    SharedWorkspaceModel,
)

T = TypeVar("T", bound=Base)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _add_and_commit(self, instance: T) -> T:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


class HouseholdRepository(BaseRepository):
    async def create_household(self, household: HouseholdModel) -> HouseholdModel:
        return await self._add_and_commit(household)

    async def get_household(self, household_id: str) -> Optional[HouseholdModel]:
        stmt = select(HouseholdModel).where(HouseholdModel.id == household_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_households_by_user(self, user_id: str) -> List[HouseholdModel]:
        stmt = (
            select(HouseholdModel)
            .join(HouseholdMemberModel)
            .where(
                HouseholdMemberModel.user_id == user_id,
                HouseholdMemberModel.is_active.is_(True),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_member(self, member: HouseholdMemberModel) -> HouseholdMemberModel:
        return await self._add_and_commit(member)

    async def get_members(self, household_id: str) -> List[HouseholdMemberModel]:
        stmt = select(HouseholdMemberModel).where(
            HouseholdMemberModel.household_id == household_id
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class DelegationRepository(BaseRepository):
    async def create_delegation(self, delegation: DelegationModel) -> DelegationModel:
        return await self._add_and_commit(delegation)

    async def get_active_delegations_for_delegatee(
        self, delegatee_id: str
    ) -> List[DelegationModel]:
        stmt = select(DelegationModel).where(
            DelegationModel.delegatee_user_id == delegatee_id,
            DelegationModel.is_active.is_(True),
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class AdvisorRepository(BaseRepository):
    async def register_advisor(self, advisor: AdvisorModel) -> AdvisorModel:
        return await self._add_and_commit(advisor)

    async def get_advisor_by_user_id(self, user_id: str) -> Optional[AdvisorModel]:
        stmt = select(AdvisorModel).where(AdvisorModel.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class WorkspaceRepository(BaseRepository):
    async def create_workspace(
        self, workspace: SharedWorkspaceModel
    ) -> SharedWorkspaceModel:
        return await self._add_and_commit(workspace)

    async def get_workspace(self, workspace_id: str) -> Optional[SharedWorkspaceModel]:
        stmt = select(SharedWorkspaceModel).where(
            SharedWorkspaceModel.id == workspace_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
