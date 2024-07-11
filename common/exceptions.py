from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrectEmailOrPasswordsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверная почта или пароль",
)

TokenExpiredException = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Авторизация истекла",
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Авторизация отсутствует",
)

IncorrectTokenFormatExpressionException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен неверного формата",
)

DownloadErrorException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Ошибка при скачивании видеоролика",
)

UrlFormatException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid url"
)
