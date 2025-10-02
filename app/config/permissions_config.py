class PermissionsConfig:
    def __init__(self):
        self.owner_only_fields : list[str] = []
        self.admin_only_fields : list[str] = []
        self.public_fields : list[str] = []