from datetime import date
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    first_name: str = Field(title='Имя', min_length=2)
    last_name: str = Field(title='Фамилия', min_length=2)
    birthdate: date = Field(title='Дата рождения')
    email: EmailStr = Field(title='Email', min_length=5)
    address: str = Field(title='Адрес', min_length=5)




class UserWithId(User):
    user_id: int = Field(title='ID')