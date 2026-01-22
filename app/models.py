from sqlalchemy import Column, Integer, Numeric, ForeignKey, Text, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from decimal import Decimal
from datetime import datetime
import uuid

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey('categories.id', ondelete="CASCADE"),
        nullable=True
    )

    parent = relationship('Category', remote_side=[id], back_populates='children')
    children = relationship('Category', back_populates='parent', cascade='all, delete-orphan')
    products = relationship('Nomenclature', back_populates='category', cascade='all, delete-orphan')


class Nomenclature(Base):
    __tablename__ = 'nomenclature'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey('categories.id', ondelete="SET NULL"),
        nullable=True
    )

    category = relationship('Category', back_populates='products')
    order_items = relationship('OrderItem', back_populates='product')


class Client(Base):
    __tablename__ = 'clients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)

    orders = relationship('Order', back_populates='client', cascade='all, delete-orphan')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey('clients.id', ondelete="CASCADE"),
        nullable=False
    )
    date = Column(DateTime, nullable=False, default=datetime.now)

    client = relationship('Client', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey('orders.id', ondelete="CASCADE"),
        nullable=False
    )
    nomenclature_id = Column(
        UUID(as_uuid=True),
        ForeignKey('nomenclature.id', ondelete="RESTRICT"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship('Order', back_populates='items')
    product = relationship('Nomenclature', back_populates='order_items')