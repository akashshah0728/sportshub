from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Season
from schemas import SeasonCreate, SeasonRead, SeasonUpdate

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.post("", response_model=SeasonRead, status_code=status.HTTP_201_CREATED)
def create_season(season_in: SeasonCreate, db: Session = Depends(get_db)):
    new_season = Season(season_year=season_in.season_year)
    db.add(new_season)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Season {season_in.season_year} already exists.",
        )
    db.refresh(new_season)
    return new_season


@router.get("/{season_id}", response_model=SeasonRead)
def read_season(season_id: int, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found.",
        )
    return season


@router.get("", response_model=list[SeasonRead])
def list_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Season).offset(skip).limit(limit).all()


@router.patch("/{season_id}", response_model=SeasonRead)
def update_season(season_id: int, season_in: SeasonUpdate, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found.",
        )

    update_data = season_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(season, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Season {season_in.season_year} already exists.",
        )
    db.refresh(season)
    return season


@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found.",
        )
    db.delete(season)
    db.commit()