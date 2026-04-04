from dataclasses import dataclass

@dataclass
class CurrentContext:
    user_id: int
    tenant_id: int