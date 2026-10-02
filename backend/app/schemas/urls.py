from pydantic import BaseModel


class CreateURLRequest(BaseModel):
    url: str


class CreateURLResponse(BaseModel):
    code: str
    short_url: str
    target_url: str


class URLInfoResponse(BaseModel):
    code: str
    short_url: str
    target_url: str
    clicks: int


class AnalyticsResponse(BaseModel):
    code: str
    clicks: int
