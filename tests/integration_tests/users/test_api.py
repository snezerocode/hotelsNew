import pytest


@pytest.fixture(scope="module")
async def delete_all_users(db_module):
    await db_module.users.delete()
    await db_module.commit()


@pytest.mark.parametrize(
    "email, password",
    [
        ("example1@email.com", "111111"),
        ("example2@email.com", "111112"),
        ("example3@email.com", "111113"),
    ],
)
async def test_register_login_logout_user(
    email,
    password,
    delete_all_users,
    authenticated_ac,
):
    response_registration = await authenticated_ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_registration.status_code == 200

    response_login = await authenticated_ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response_login.status_code == 200

    jwt = authenticated_ac.cookies["access_token"]

    assert jwt

    response_me = await authenticated_ac.post("/auth/me")
    assert response_me.status_code == 200
    response_data = response_me.json()
    assert response_data["email"] == email

    response_logout = await authenticated_ac.get("/auth/logout")

    assert response_logout.status_code == 200
    assert "access_token" not in authenticated_ac.cookies
