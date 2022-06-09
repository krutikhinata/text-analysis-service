import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel


def form_body_model(cls: Type[BaseModel]):
    """Adds an as_form class method to decorated models.

    The as_form class method can be used with FastAPI endpoints to treat the
    model as a form body, eliminating the need to have all the form fields
    described in the endpoint function definition.

    Example usage:
    @form_body_model
    class MessageIn(BaseModel):
        from_number: str = Form(
            ...,
            alias='FromNumber',
            example='+18445551212',
            description='Sender Phone Number',
        )
        to_number: str = Form(
            ...,
            alias='ToNumber',
            example='+18885551212',
            description='Recipient Phone Number',
        )
        body: str = Form(
            ...,
            alias='Body',
            example='Happy Birthday',
            description='Text message body',
        )
        delivery_time: Optional[datetime.datetime] = Form(
            '',
            alias='ApiVersion',
            example='2021-03-10T07:00:00-0500',
            description='Scheduled time for delivery (default is immediate)',
        )
        log_comment: Optional[str] = Form(
            '',
            alias='Body',
            example='This is a test',
            description='Comments that are captured in the log',
        )

    @route.post('/message/schedule')
    async def schedule_message(data: MessageIn = Depends(MessageIn.as_form)):
        # data is a Pydantic model with parsed form post data
        print(data.dict())
        return data.dict()
    """
    new_params = []
    for field in cls.__fields__.values():
        new_params.append(
            inspect.Parameter(
                field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                annotation=cls.__annotations__[field.name],
                default=(
                    Form(
                        field.default if not field.required else ...,
                        description=field.field_info.description,
                        alias=field.alias,
                        ge=getattr(field, "ge", None),
                        gt=getattr(field, "gt", None),
                        le=getattr(field, "le", None),
                        lt=getattr(field, "lt", None),
                        max_length=getattr(field, "max_length", None),
                        min_length=getattr(field, "min_length", None),
                        regex=getattr(field, "regex", None),
                        title=getattr(field, "title", None),
                        media_type=getattr(field, "media_type", None),
                        **field.field_info.extra,
                    )
                ),
            )
        )

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)

    return cls
