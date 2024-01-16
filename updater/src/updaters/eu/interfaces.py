from pydantic import BaseModel


class EsiMetric(BaseModel):
    """Represents interface of EU ESI metric"""
    code: str
    name: str