# File: tests/test_permissions_register.py

import pytest
from app.config.permissions_config import PermissionsRegister, Permissions, AllUserRolePermissions
from app.config.user_roles import UserRole


# ---------------------------------------------------------------------------
# Dummy classes for testing
# ---------------------------------------------------------------------------

class BaseModel:
    """Base model used for inheritance tests."""
    pass


class ChildModel(BaseModel):
    """Child model used to validate inheritance behavior."""
    pass


# ---------------------------------------------------------------------------
# Unit test suite for PermissionsRegister
# ---------------------------------------------------------------------------

class TestPermissionsRegister:

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Ensure the global registry is clean before and after each test."""
        PermissionsRegister._registry.clear()
        yield
        PermissionsRegister._registry.clear()

    # -----------------------------------------------------------------------
    # Basic registration behavior
    # -----------------------------------------------------------------------

    def test_register_creates_new_entry(self):
        """Should create a new registry entry for a model and role."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["name", "email"])
        assert "BaseModel" in PermissionsRegister._registry
        assert UserRole.ADMIN in PermissionsRegister._registry["BaseModel"]
        assert PermissionsRegister._registry["BaseModel"][UserRole.ADMIN]["attributes"] == {"name", "email"}

    def test_register_merges_attributes_when_overwrite_false(self):
        """Should merge new attributes if overwrite=False."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["a", "b"])
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["c"], overwrite=False)

        attrs = PermissionsRegister._registry["BaseModel"][UserRole.ADMIN]["attributes"]
        assert attrs == {"a", "b", "c"}

    def test_register_overwrites_attributes_when_overwrite_true(self):
        """Should replace existing attributes if overwrite=True."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["x", "y"])
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["z"], overwrite=True)

        attrs = PermissionsRegister._registry["BaseModel"][UserRole.ADMIN]["attributes"]
        assert attrs == {"z"}
        assert PermissionsRegister._registry["BaseModel"][UserRole.ADMIN]["overwrite"] is True

    # -----------------------------------------------------------------------
    # Permission retrieval
    # -----------------------------------------------------------------------

    def test_get_permissions_returns_direct_attributes(self):
        """Should return attributes registered directly for a model and role."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["id", "name"])
        result = PermissionsRegister.get_permissions(BaseModel, UserRole.ADMIN)
        assert result == {"id", "name"}

    def test_get_permissions_merges_attributes_from_bases(self):
        """Should merge attributes from base classes in the MRO chain."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["a", "b"])
        PermissionsRegister.register(ChildModel, UserRole.ADMIN, ["c"])

        result = PermissionsRegister.get_permissions(ChildModel, UserRole.ADMIN)
        assert result == {"a", "b", "c"}

    def test_get_permissions_child_overwrites_base(self):
        """Child with overwrite=True should ignore base attributes."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["a", "b"])
        PermissionsRegister.register(ChildModel, UserRole.ADMIN, ["x"], overwrite=True)

        result = PermissionsRegister.get_permissions(ChildModel, UserRole.ADMIN)
        assert result == {"x"}

    def test_get_permissions_for_unregistered_model_returns_empty_set(self):
        """Should return an empty set if the model has no registered permissions."""
        result = PermissionsRegister.get_permissions(BaseModel, UserRole.ADMIN)
        assert result == set()

    # -----------------------------------------------------------------------
    # Access checking
    # -----------------------------------------------------------------------

    def test_has_access_returns_true_for_allowed_attribute(self):
        """Should return True if the attribute is in the allowed set."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["visible"])
        assert PermissionsRegister.has_access(BaseModel, UserRole.ADMIN, "visible") is True

    def test_has_access_returns_false_for_disallowed_attribute(self):
        """Should return False if the attribute is not in the allowed set."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["allowed"])
        assert PermissionsRegister.has_access(BaseModel, UserRole.ADMIN, "forbidden") is False

    # -----------------------------------------------------------------------
    # Multiple roles and models
    # -----------------------------------------------------------------------

    def test_register_multiple_roles_for_same_model(self):
        """Different roles on the same model should have independent permissions."""
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["a", "b"])
        PermissionsRegister.register(BaseModel, UserRole.USER, ["x"])

        admin_attrs = PermissionsRegister.get_permissions(BaseModel, UserRole.ADMIN)
        user_attrs = PermissionsRegister.get_permissions(BaseModel, UserRole.USER)

        assert admin_attrs == {"a", "b"}
        assert user_attrs == {"x"}
        assert admin_attrs != user_attrs

    def test_integration_multiple_models_and_roles(self):
        """Full integration test across multiple models and roles."""
        class AnotherModel:
            pass

        # Register various combinations
        PermissionsRegister.register(BaseModel, UserRole.ADMIN, ["a1", "a2"])
        PermissionsRegister.register(BaseModel, UserRole.USER, ["a3"])
        PermissionsRegister.register(AnotherModel, UserRole.ADMIN, ["b1"], overwrite=True)

        # Validate consistency
        assert PermissionsRegister.has_access(BaseModel, UserRole.ADMIN, "a1") is True
        assert PermissionsRegister.has_access(BaseModel, UserRole.USER, "a2") is False
        assert PermissionsRegister.has_access(AnotherModel, UserRole.ADMIN, "b1") is True
        assert PermissionsRegister.has_access(AnotherModel, UserRole.ADMIN, "b2") is False


# ---------------------------------------------------------------------------
# Tests for decorators
# ---------------------------------------------------------------------------

class TestDecorators:

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Ensure registry is clean before and after each test."""
        PermissionsRegister._registry.clear()
        yield
        PermissionsRegister._registry.clear()

    def test_permissions_decorator_registers_attributes(self):
        """Decorator @Permissions should register attributes correctly."""
        @Permissions(UserRole.ADMIN, ["id", "name"])
        class Demo:
            pass

        attrs = PermissionsRegister.get_permissions(Demo, UserRole.ADMIN)
        assert attrs == {"id", "name"}

    def test_all_user_role_permissions_registers_for_all_roles(self):
        """Decorator @AllUserRolePermissions should register for all roles."""
        @AllUserRolePermissions(["id", "email"])
        class Demo:
            pass

        for role in UserRole:
            assert PermissionsRegister.has_access(Demo, role, "id")
            assert PermissionsRegister.has_access(Demo, role, "email")
