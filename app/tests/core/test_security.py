import pytest

from app.core.security import (
    hash_password, verify_password, 
    encode_jwt_token, decode_jwt_token, 
    JWTType
)


def test_password_verify():
    plain_password = "somepassword123"
    other_password = "ceiwqcei"
    hashed_password = hash_password(plain_password)
    assert plain_password != hashed_password, "Hashed and plain password should not be the same"
    assert verify_password(plain_password, hashed_password), "Can not verify valid password"
    assert not verify_password(other_password, hashed_password), "Invalid password verified as valid"

@pytest.mark.parametrize("jwt_type", ("access", "secret"))
def test_jwt_decode(jwt_type: JWTType):
    data = {
        "first": "data",
        "help": 123
    }
    encoded = encode_jwt_token(data=data, type_=jwt_type)
    decoded_data = decode_jwt_token(encoded=encoded["token"], type_=jwt_type)
    assert decoded_data == data, "Decoded data not the same"
