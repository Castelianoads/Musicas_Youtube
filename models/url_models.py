from pydantic import BaseModel

class URLItem(BaseModel):
  url: str

class URLList(BaseModel):
  urls: list[str]
