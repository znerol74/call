from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.phone_number import PhoneNumber
from app.models.agent import Agent
from app.schemas.phone_number import PhoneNumberCreate, PhoneNumberUpdate, PhoneNumberResponse

router = APIRouter()


@router.post("/", response_model=PhoneNumberResponse, status_code=status.HTTP_201_CREATED)
async def create_phone_number(
    phone_data: PhoneNumberCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new phone number"""
    # Check if phone number already exists
    result = await db.execute(
        select(PhoneNumber).where(PhoneNumber.phone_number == phone_data.phone_number)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already exists"
        )

    # Verify agent belongs to user if agent_id provided
    if phone_data.agent_id:
        agent_result = await db.execute(
            select(Agent).where(Agent.id == phone_data.agent_id, Agent.user_id == current_user.id)
        )
        if not agent_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )

    new_phone_number = PhoneNumber(
        user_id=current_user.id,
        agent_id=phone_data.agent_id,
        phone_number=phone_data.phone_number,
        provider=phone_data.provider,
        provider_config=phone_data.provider_config
    )

    db.add(new_phone_number)
    await db.commit()
    await db.refresh(new_phone_number)

    return new_phone_number


@router.get("/", response_model=List[PhoneNumberResponse])
async def list_phone_numbers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all phone numbers for the current user"""
    result = await db.execute(
        select(PhoneNumber).where(PhoneNumber.user_id == current_user.id)
    )
    phone_numbers = result.scalars().all()
    return phone_numbers


@router.put("/{phone_number_id}", response_model=PhoneNumberResponse)
async def update_phone_number(
    phone_number_id: int,
    phone_data: PhoneNumberUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a phone number (e.g., assign to different agent)"""
    result = await db.execute(
        select(PhoneNumber).where(
            PhoneNumber.id == phone_number_id,
            PhoneNumber.user_id == current_user.id
        )
    )
    phone_number = result.scalar_one_or_none()

    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number not found"
        )

    # Verify agent belongs to user if agent_id provided
    if phone_data.agent_id:
        agent_result = await db.execute(
            select(Agent).where(Agent.id == phone_data.agent_id, Agent.user_id == current_user.id)
        )
        if not agent_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )

    # Update fields
    update_data = phone_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(phone_number, field, value)

    await db.commit()
    await db.refresh(phone_number)

    return phone_number


@router.delete("/{phone_number_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_phone_number(
    phone_number_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a phone number"""
    result = await db.execute(
        select(PhoneNumber).where(
            PhoneNumber.id == phone_number_id,
            PhoneNumber.user_id == current_user.id
        )
    )
    phone_number = result.scalar_one_or_none()

    if not phone_number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone number not found"
        )

    await db.delete(phone_number)
    await db.commit()
