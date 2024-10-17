from fastapi import Depends, Query
from typing import Annotated
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[ int | None, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[ int | None, Query(3, description="Количество отелей на странице", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]