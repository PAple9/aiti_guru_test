from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Order, OrderItem, Nomenclature

router = APIRouter(prefix="/api/v1", tags=["orders"])


@router.get("/orders/{order_id}/total")
async def get_order_total(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    result = await db.execute(
        select(func.sum(OrderItem.quantity * OrderItem.price))
        .where(OrderItem.order_id == order_id)
    )
    total = result.scalar()

    return {"order_id": order_id, "total_amount": float(total or 0)}


@router.post("/orders/{order_id}/add-product")
async def add_product_to_order(
        order_id: str,
        product_id: str,
        quantity: int,
        db: AsyncSession = Depends(get_db)
):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Количество должно быть > 0")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    result = await db.execute(select(Nomenclature).where(Nomenclature.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    if product.quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Недостаточно товара. Доступно: {product.quantity}"
        )

    result = await db.execute(
        select(OrderItem)
        .where(OrderItem.order_id == order_id, OrderItem.nomenclature_id == product_id)
    )
    existing_item = result.scalar_one_or_none()

    try:
        product.quantity -= quantity

        if existing_item:
            existing_item.quantity += quantity
        else:
            order_item = OrderItem(
                order_id=order_id,
                nomenclature_id=product_id,
                quantity=quantity,
                price=product.price
            )
            db.add(order_item)

        await db.commit()

        return {
            "success": True,
            "message": "Товар добавлен",
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity
        }

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка: {str(e)}")
