from pydantic import BaseModel

class LogInDTO(BaseModel):
    email: str = "jonasaray12@gmail.com"
    password: str = "yovita1234"


class LogInResponse(BaseModel):
    id: int = 1
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzAyODY0NDMsInVzZXJuYW1lIjoiam9uYXNhcmExMkBnbWFpbC5jb20ifQ.YWSyBd1sRM6SGOTwrkWl6axX0UWYik_P5SkPuUPWnI8"