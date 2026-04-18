import httpx
from app.config.settings import settings


def _raise_for_status(response: httpx.Response) -> dict:
    if response.status_code != 200:
        raise ValueError("Failed to verify OAuth token")
    return response.json()


class OAuthService:
    @staticmethod
    async def verify_google_token(access_token: str) -> dict:
        url = "https://oauth2.googleapis.com/tokeninfo"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params={"id_token": access_token})
        data = _raise_for_status(response)

        if data.get("aud") != settings.GOOGLE_CLIENT_ID:
            raise ValueError("Invalid Google ID token audience.")
        if data.get("email_verified") not in ("true", True, 1):
            raise ValueError("Google email is not verified.")

        return {
            "email": data.get("email"),
            "name": data.get("name") or data.get("email").split("@")[0],
        }

    @staticmethod
    async def verify_linkedin_token(access_token: str) -> dict:
        headers = {"Authorization": f"Bearer {access_token}"}
        async with httpx.AsyncClient(timeout=10) as client:
            profile_response = await client.get("https://api.linkedin.com/v2/me", headers=headers)
            email_response = await client.get(
                "https://api.linkedin.com/v2/emailAddress",
                headers=headers,
                params={"q": "members", "projection": "(elements*(handle~))"},
            )

        profile = _raise_for_status(profile_response)
        email_data = _raise_for_status(email_response)

        email = None
        elements = email_data.get("elements")
        if elements and isinstance(elements, list):
            email = elements[0].get("handle~", {}).get("emailAddress")

        first_name = profile.get("localizedFirstName")
        last_name = profile.get("localizedLastName")
        name = " ".join(part for part in [first_name, last_name] if part).strip()

        if not email:
            raise ValueError("LinkedIn profile did not return an email address.")

        return {"email": email, "name": name or email.split("@")[0]}
