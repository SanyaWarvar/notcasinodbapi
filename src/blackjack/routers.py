from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from src.blackjack.models.card import Card
from src.blackjack.models.table import Tables, Table
from src.database import get_async_session
from src.users.models import User, Token
from sqlalchemy import select
from src.tokens.tokens import check_token_valid

router = APIRouter(
    prefix="/bj",
    tags=["blackjack"]
)


@router.post("/create_table", status_code=200)
async def create_table(bet: int, access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")

    token: Token = await session.scalar(select(Token).where(Token.access_token == access_token))
    user: User = await session.scalar(select(User).where(token.user_id == User.id))
    t: Tables = await session.scalar(select(Tables).where(token.user_id == Tables.user_id))

    if t is not None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Blackjack table for {user.username} already exist!"
        )

    if not user.balance >= bet:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Balance must be higher than bet!")

    table = Table(bet)

    session.add(Tables(
        user_id=user.id,
        main_hand=" ".join(list(map(str, table.main_hand.cards))),
        dealer_hand=" ".join(list(map(str, table.dealer_hand.cards))),
        bet=table.bet,
        deck=" ".join(list(map(str, table.deck)))
    ))

    await session.commit()
    return {
        "player_cards": " ".join(list(map(str, table.main_hand.cards))),
        "dealer_cards": " ".join(list(map(str, table.dealer_hand.cards)))
    }


@router.get("/add_card", status_code=200)
async def add_card(access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")

    token: Token = await session.scalar(select(Token).where(Token.access_token == access_token))
    t: Tables = await session.scalar(select(Tables).where(token.user_id == Tables.user_id))

    if t is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Blackjack table doesn't exist!"
        )

    player_cards = list(map(Card.get_from_str, t.main_hand.split(" ")))
    dealer_cards = list(map(Card.get_from_str, t.dealer_hand.split(" ")))
    deck = list(map(Card.get_from_str, t.deck.split(" ")))

    table = Table(t.bet, player_cards=player_cards, dealer_cards=dealer_cards, deck=deck)
    table.main_hand.add_card(table.deck)

    t.main_hand = " ".join(list(map(str, table.main_hand.cards)))
    t.dealer_hand = " ".join(list(map(str, table.dealer_hand.cards)))
    t.deck = " ".join(list(map(str, table.deck)))

    session.add(t)

    await session.commit()

    return {
        "player_cards": " ".join(list(map(str, table.main_hand.cards))),
        "dealer_cards": " ".join(list(map(str, table.dealer_hand.cards)))
    }


@router.get("/stand", status_code=200)
async def stand(access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")

    token: Token = await session.scalar(select(Token).where(Token.access_token == access_token))
    t: Tables = await session.scalar(select(Tables).where(token.user_id == Tables.user_id))

    if t is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Blackjack table doesn't exist!"
        )

    player_cards = list(map(Card.get_from_str, t.main_hand.split(" ")))
    dealer_cards = list(map(Card.get_from_str, t.dealer_hand.split(" ")))
    deck = list(map(Card.get_from_str, t.deck.split(" ")))

    table = Table(t.bet, player_cards=player_cards, dealer_cards=dealer_cards, deck=deck)
    table.main_hand.is_double = t.is_double
    table.dealer_turn()

    result = table.result()

    user: User = await session.scalar(select(User).where(token.user_id == User.id))
    user.balance += result

    session.add(user)
    await session.commit()

    await session.delete(t)
    await session.commit()

    return {
        "result:": result,
        "dealer_cards:": " ".join(list(map(str, table.main_hand.cards))),
        "player_hand": " ".join(list(map(str, table.dealer_hand.cards)))
    }


@router.get("/double", status_code=200)
async def double(access_token: str, session=Depends(get_async_session)):
    if not await check_token_valid(access_token, session):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Token isn't valid!")

    token: Token = await session.scalar(select(Token).where(Token.access_token == access_token))
    t: Tables = await session.scalar(select(Tables).where(token.user_id == Tables.user_id))

    if t is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Blackjack table doesn't exist!"
        )

    if not t.is_double:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"You can't do double!"
        )

    player_cards = list(map(Card.get_from_str, t.main_hand.split(" ")))
    dealer_cards = list(map(Card.get_from_str, t.dealer_hand.split(" ")))
    deck = list(map(Card.get_from_str, t.deck.split(" ")))

    table = Table(t.bet, player_cards=player_cards, dealer_cards=dealer_cards, deck=deck)

    table.main_hand.double(table.deck)
    t.is_double = True

    t.main_hand = " ".join(list(map(str, table.main_hand.cards)))
    t.dealer_hand = " ".join(list(map(str, table.dealer_hand.cards)))
    t.deck = " ".join(list(map(str, table.deck)))

    session.add(t)

    await session.commit()

    return await stand(access_token, session)
