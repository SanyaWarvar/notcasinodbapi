import ast
from random import choice
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.database import get_async_session
from src.users.models import User, Token
from sqlalchemy import select
from src.tokens.tokens import check_token_valid
from src.roulette.config import roulette_numbers, multipliers

router = APIRouter(
    prefix="/roulette",
    tags=["roulette"]
)


@router.post("/play")
async def play(user_token: str, bet, session=Depends(get_async_session)):
    if not await check_token_valid(user_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")

    bet = ast.literal_eval(bet)
    money_delta = -1 * sum(bet.values())  # todo check values types

    if min(bet.values()) <= 0:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="You cann't place negative or zero bet!")

    user_id: int = await session.scalar(select(Token.user_id).where(Token.access_token == user_token))
    user: User = await session.scalar(select(User).where(User.id == user_id))

    if money_delta > user.balance:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User balance must be >= sum of bet!")

    win_number = choice(roulette_numbers)
    characteristic = dict()

    if roulette_numbers.index(win_number) % 2 == 0:
        if win_number == 0:
            characteristic["color"] = "zero"
        else:
            characteristic["color"] = "black"
    else:
        characteristic["color"] = "red"

    if win_number % 2 == 0:
        if win_number == 0:
            characteristic["parity"] = "zero"
        else:
            characteristic["parity"] = "even"
    else:
        characteristic["parity"] = "odd"

    characteristic["twelve"] = win_number // 12 + 1
    if win_number in [12, 24, 36]:
        characteristic["twelve"] -= 1
    elif win_number == 0:
        characteristic["twelve"] = 0

    characteristic["half"] = win_number // 18 + 1
    if win_number in [18, 36]:
        characteristic["half"] -= 1
    elif win_number == 0:
        characteristic["half"] = 0



    for k, v in bet.items():
        if k not in multipliers:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Bet list isn't valid! {k} not in bet "
                                                                         f"possible list")
        try:
            if int(k) == win_number:
                money_delta += v * multipliers[k]
        except ValueError:
            if k in ["red", "black"]:
                if characteristic["color"] == k:
                    money_delta += v * multipliers[k]
            if k in ["odd", "even"]:
                if characteristic["parity"] == k:
                    money_delta += v * multipliers[k]
            if k in ["1-18", "19-36"]:
                if characteristic["half"] == ["1-18", "19-36"].index(k) + 1:
                    money_delta += v * multipliers[k]
            if k in ["1-12", "13-24", "25-36"]:
                if characteristic["twelve"] == ["1-12", "13-24", "25-36"].index(k) + 1:
                    money_delta += v * multipliers[k]

    user.balance += money_delta
    await session.commit()

    return {"win_number": win_number, "money_delta": money_delta}
