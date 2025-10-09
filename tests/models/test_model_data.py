# tests/test_model_data.py

import pytest
from datetime import datetime, timezone
from bson import ObjectId
from uuid import UUID
import time
from app.models.model_data import ModelData

# ------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------

@pytest.fixture
def sample_model():
    """Fixture that returns a fresh ModelData instance for each test."""
    return ModelData(created_by=ObjectId(), owner_id=ObjectId())


# ------------------------------------------------------------
# Initialization tests
# ------------------------------------------------------------

def test_model_initialization_defaults(sample_model):
    """Ensure model initializes all fields with correct default values."""
    assert isinstance(sample_model.internal_id, ObjectId)
    assert isinstance(sample_model.public_id, str)
    assert isinstance(UUID(sample_model.public_id), UUID)
    assert isinstance(sample_model.created_at, datetime)
    assert isinstance(sample_model.updated_at, datetime)
    assert sample_model.is_active is True


def test_model_public_id_is_uuid(sample_model):
    """Ensure public_id is a valid UUID string."""
    uuid_obj = UUID(sample_model.public_id)
    assert str(uuid_obj) == sample_model.public_id


def test_model_internal_id_is_objectid(sample_model):
    """Ensure internal_id is a valid Mongo ObjectId."""
    assert isinstance(sample_model.internal_id, ObjectId)


# ------------------------------------------------------------
# Timestamp tests
# ------------------------------------------------------------

def test_update_timestamp_changes_updated_at(sample_model):
    """Ensure updated_at changes when update_timestamp is called."""
    old_time = sample_model.updated_at
    time.sleep(0.01)
    sample_model.update_timestamp()
    assert sample_model.updated_at > old_time


def test_update_timestamp_preserves_created_at(sample_model):
    """Ensure created_at remains unchanged when updating timestamp."""
    old_created = sample_model.created_at
    time.sleep(0.01)
    sample_model.update_timestamp()
    assert sample_model.created_at == old_created


# ------------------------------------------------------------
# Soft delete & restore
# ------------------------------------------------------------

def test_soft_delete_sets_is_active_false(sample_model):
    """Ensure soft_delete marks the record as inactive."""
    sample_model.soft_delete()
    assert sample_model.is_active is False


def test_soft_delete_updates_timestamp(sample_model):
    """Ensure updated_at changes when record is soft deleted."""
    old_time = sample_model.updated_at
    time.sleep(0.01)
    sample_model.soft_delete()
    assert sample_model.updated_at > old_time


def test_restore_sets_is_active_true(sample_model):
    """Ensure restore reactivates the record."""
    sample_model.is_active = False
    sample_model.restore()
    assert sample_model.is_active is True


def test_restore_updates_timestamp(sample_model):
    """Ensure updated_at changes when record is restored."""
    sample_model.is_active = False
    old_time = sample_model.updated_at
    time.sleep(0.01)
    sample_model.restore()
    assert sample_model.updated_at > old_time


# ------------------------------------------------------------
# Ownership & traceability
# ------------------------------------------------------------

def test_is_owned_by_returns_true_for_owner(sample_model):
    """Ensure is_owned_by returns True for the correct owner."""
    assert sample_model.is_owned_by(sample_model.owner_id)


def test_is_owned_by_returns_false_for_different_user(sample_model):
    """Ensure is_owned_by returns False for different user."""
    other_user = ObjectId()
    assert not sample_model.is_owned_by(other_user)


def test_is_created_by_returns_true_for_creator(sample_model):
    """Ensure is_created_by returns True for the creator."""
    assert sample_model.is_created_by(sample_model.created_by)


def test_set_owner_updates_owner_and_timestamp(sample_model):
    """Ensure set_owner updates owner_id and updated_at."""
    new_owner = ObjectId()
    old_time = sample_model.updated_at
    time.sleep(0.01)
    sample_model.set_owner(new_owner)
    assert sample_model.owner_id == new_owner
    assert sample_model.updated_at > old_time


def test_transfer_ownership_changes_owner(sample_model):
    """Ensure transfer_ownership assigns a new owner and updates timestamp."""
    new_owner = ObjectId()
    old_time = sample_model.updated_at
    time.sleep(0.01)
    sample_model.transfer_ownership(new_owner)
    assert sample_model.owner_id == new_owner
    assert sample_model.updated_at > old_time


# ------------------------------------------------------------
# Serialization and data exposure
# ------------------------------------------------------------

def test_to_public_dict_excludes_sensitive_fields(sample_model):
    """Ensure sensitive fields are excluded from public dict."""
    result = ModelData._to_public_dict(sample_model, exclude_fields=["internal_id", "created_by"])
    assert "internal_id" not in result
    assert "created_by" not in result


def test_to_public_dict_respects_exclude_fields_param(sample_model):
    """Ensure exclude_fields parameter works as expected."""
    result = ModelData._to_public_dict(sample_model, exclude_fields=["owner_id"])
    assert "owner_id" not in result


def test_to_owner_dict_includes_expected_fields(sample_model):
    """Ensure owner dict excludes only internal fields."""
    result = ModelData.to_owner_dict(sample_model)
    assert "_id" not in result
    assert "internal_id" not in result
    assert "public_id" in result


def test_to_owner_dict_preserves_all_non_sensitive_data(sample_model):
    """Ensure non-sensitive fields are preserved in owner dict."""
    result = ModelData.to_owner_dict(sample_model)
    assert result["owner_id"] == sample_model.owner_id
    assert result["is_active"] == sample_model.is_active


# ------------------------------------------------------------
# Representation
# ------------------------------------------------------------

def test_repr_contains_class_and_ids(sample_model):
    """Ensure __repr__ contains key identifiers."""
    repr_str = repr(sample_model)
    assert sample_model.public_id in repr_str
    assert str(sample_model.internal_id) in repr_str
    assert sample_model.__class__.__name__ in repr_str


def test_str_returns_readable_format(sample_model):
    """Ensure __str__ returns readable class name and public_id."""
    result = str(sample_model)
    assert sample_model.public_id in result
    assert sample_model.__class__.__name__ in result


# ------------------------------------------------------------
# Edge cases & robustness
# ------------------------------------------------------------

def test_soft_delete_on_already_deleted_model_is_idempotent(sample_model):
    """Ensure soft_delete can be safely called multiple times."""
    sample_model.soft_delete()
    sample_model.soft_delete()
    assert sample_model.is_active is False


def test_restore_on_already_active_model_is_idempotent(sample_model):
    """Ensure restore can be safely called multiple times."""
    sample_model.restore()
    sample_model.restore()
    assert sample_model.is_active is True


def test_to_public_dict_with_no_exclude_fields_does_not_fail(sample_model):
    """Ensure method handles None as exclude_fields."""
    result = ModelData._to_public_dict(sample_model, exclude_fields=[])
    assert isinstance(result, dict)
    assert "public_id" in result


def test_set_owner_with_none_user_does_not_crash(sample_model):
    """Ensure set_owner can handle None as user_id."""
    sample_model.set_owner(None)
    assert sample_model.owner_id is None