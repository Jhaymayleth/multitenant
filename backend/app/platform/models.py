"""Modelos ORM del schema global 'platform'.

Basado en docs/07-MODELO-DATOS.md (Sección 2).
Este schema es compartido por toda la plataforma SaaS y alberga la identidad global,
tenants, membresías, planes, suscripciones, verificaciones y claves de idempotencia.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    password_hash = Column(Text, nullable=True)
    google_sub = Column(Text, unique=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'active', 'disabled')"),
        nullable=False,
        default="pending",
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    memberships = relationship("TenantMembership", back_populates="user", cascade="all, delete-orphan")


class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    legal_name = Column(String(255), nullable=True)
    schema_name = Column(String(63), unique=True, nullable=False, index=True)  # tenant_<12hex>
    status = Column(
        String(30),
        CheckConstraint(
            "status IN ('provisioning', 'provisioning_failed', 'pending_verification', 'active', 'suspended', 'cancelled')"
        ),
        nullable=False,
        default="provisioning",
    )
    timezone = Column(String(50), nullable=False, default="America/Bogota")
    currency = Column(String(3), nullable=False, default="COP")
    contact_email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    activated_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    memberships = relationship("TenantMembership", back_populates="tenant")
    subscription = relationship("Subscription", back_populates="tenant", uselist=False)


class TenantMembership(Base):
    __tablename__ = "tenant_memberships"
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id", name="uq_tenant_user_membership"),
        {"schema": "platform"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("platform.tenants.id", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("platform.users.id", ondelete="CASCADE"), nullable=False)
    role = Column(
        String(20),
        CheckConstraint("role IN ('owner', 'admin', 'waiter', 'cashier', 'cook')"),
        nullable=False,
    )
    status = Column(
        String(20),
        CheckConstraint("status IN ('invited', 'active', 'disabled', 'revoked')"),
        nullable=False,
        default="invited",
    )
    created_by = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", back_populates="memberships", foreign_keys=[user_id])
    tenant = relationship("Tenant", back_populates="memberships")


class PlatformAdmin(Base):
    __tablename__ = "platform_admins"
    __table_args__ = {"schema": "platform"}

    user_id = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), primary_key=True)
    level = Column(
        String(20),
        CheckConstraint("level IN ('support', 'admin')"),
        nullable=False,
        default="support",
    )
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret_encrypted = Column(Text, nullable=True)
    last_access_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class Plan(Base):
    __tablename__ = "plans"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(50), unique=True, nullable=False)  # basic, intermediate, advanced
    name = Column(String(100), nullable=False)
    capabilities = Column(JSONB, nullable=False, default=dict)
    limits = Column(JSONB, nullable=False, default=dict)
    price_cents = Column(Integer, nullable=False, default=0)
    currency = Column(String(3), nullable=False, default="COP")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("platform.tenants.id"), unique=True, nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("platform.plans.id"), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'trialing', 'active', 'past_due', 'suspended', 'cancelled')"),
        nullable=False,
        default="pending",
    )
    started_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    grace_until = Column(DateTime(timezone=True), nullable=True)
    activated_by = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    tenant = relationship("Tenant", back_populates="subscription")
    plan = relationship("Plan")


class SubscriptionInvoice(Base):
    __tablename__ = "subscription_invoices"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("platform.subscriptions.id"), nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'paid', 'void')"),
        nullable=False,
        default="pending",
    )
    method = Column(String(20), nullable=True)  # manual, transfer, card
    reference = Column(String(255), nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    registered_by = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class TenantVerification(Base):
    __tablename__ = "tenant_verifications"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("platform.tenants.id"), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('pending', 'approved', 'rejected')"),
        nullable=False,
        default="pending",
    )
    business_name = Column(String(255), nullable=False)
    tax_id = Column(String(50), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    documents = Column(JSONB, nullable=True)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=False)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class VerificationCode(Base):
    __tablename__ = "verification_codes"
    __table_args__ = {"schema": "platform"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("platform.users.id"), nullable=False)
    purpose = Column(
        String(30),
        CheckConstraint("purpose IN ('employee_activation', 'email_verification', 'password_reset')"),
        nullable=False,
    )
    code_hash = Column(Text, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    attempts = Column(SmallInteger, default=0, nullable=False)
    consumed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)


class GlobalIdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    __table_args__ = (
        UniqueConstraint("scope", "key", name="uq_platform_idempotency_scope_key"),
        {"schema": "platform"},
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scope = Column(String(100), nullable=False)  # platform:create_tenant
    key = Column(String(255), nullable=False)
    request_hash = Column(String(64), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('in_progress', 'completed', 'failed')"),
        nullable=False,
    )
    response_status = Column(Integer, nullable=True)
    response_body = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

