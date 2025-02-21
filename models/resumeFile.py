from pydantic import BaseModel, Field

class ResumeFile(BaseModel):
    Resume_filepath: str = Field("/path/to/folder")
    Jobdesc_filepath: str = Field("/path/to/folder")
    Keyword: str
    Query: str = Field("e.g: pick best candidate")

    class Config:
        orm_mode = True
