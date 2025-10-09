

class OwnershipConfig:
    def __init__(
        self,
        allow_ownership_transfer: bool = True
    ):
        self.allow_ownership_transfer: bool = allow_ownership_transfer

    def ownership_check(self):
        pass
