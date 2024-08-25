from typing import Annotated

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

uuid = Annotated[UUID, mapped_column(UUID(as_uuid=True))]
uuid_pk = Annotated[
    UUID,
    mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        server_default=func.uuid_generate_v4(),
    ),
]
