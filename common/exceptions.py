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
    status_code=status.HTTP_400_BAD_REQUEST, detail="Данный URL не поддерживается"
)

RegexEmailException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный формат почты"
)

"""
Никнейм может содержать от 3 до 30 символов, которые могут быть латинскими буквами, цифрами, подчеркиваниями или тире.
"""
RegexUserNameException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный формат никнейма"
)

"""
Состоит как минимум из 8 символов.
Включает только латинские буквы (как строчные, так и заглавные), цифры и перечисленные специальные символы @$!%*?&.
"""
RegexPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Неправильный формат пароля"
)

UnknownException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Неизвестная ошибка"
)

VideoNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Видео с таким ID не найдено"
)
