from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String(64), nullable=True)
    first_name = Column(String(64))
    last_name = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    character = relationship("Character", back_populates="user", uselist=False)
    inventory = relationship("Inventory", back_populates="user")

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True)
    name = Column(String(32), default="Adventurer")
    level = Column(Integer, default=1)
    exp = Column(Integer, default=0)
    gold = Column(Integer, default=100)
    hp = Column(Integer, default=100)
    max_hp = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    skill_points = Column(Integer, default=0)
    weapon_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    armor_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    last_fight = Column(DateTime, nullable=True)
    last_daily = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="character")
    weapon = relationship("Item", foreign_keys=[weapon_id])
    armor = relationship("Item", foreign_keys=[armor_id])

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    type = Column(String(32))  # weapon, armor, consumable
    value = Column(Integer)     # bonus attack/defense atau heal amount
    price = Column(Integer)
    description = Column(String(256))

class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)

    user = relationship("User", back_populates="inventory")
    item = relationship("Item")

class Monster(Base):
    __tablename__ = "monsters"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    level = Column(Integer)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    exp_reward = Column(Integer)
    gold_reward = Column(Integer)
    min_level = Column(Integer, default=1)
