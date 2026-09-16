import sys

from firebase_admin import auth

from app.integrations.firebase import initialize_firebase


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/set_admin.py <firebase-user-uid>"
        )
        raise SystemExit(1)

    uid = sys.argv[1]

    initialize_firebase()

    auth.set_custom_user_claims(
        uid,
        {"admin": True},
    )

    print(f"Admin claim assigned to user: {uid}")


if __name__ == "__main__":
    main()