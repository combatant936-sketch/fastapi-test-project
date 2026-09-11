from src.auth.schema import UserCreate
auth_prefix=f"/api/v1/auth"

def test_user_creation(fake_session,fake_user_service,test_client):
    signup_data={
        "username":"waqas",
        "first_name":"waqas",
        "last_name":"khan",
        
        "email":"waqawwaasdadsdaws@sdSADsdasdaa.com",
        "password":"waqassss"
        }

    response=test_client.post(url=f"{auth_prefix}/sign-up",json=signup_data)

    userCreate=UserCreate(**signup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(signup_data["email"],fake_session)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.create_user_called_once_with(userCreate,fake_session)
