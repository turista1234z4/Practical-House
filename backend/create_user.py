from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User

def create_user(name, email, password):
    db = SessionLocal()

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print("❌ Email já existe:", existing.email)
        return

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    print("✅ Usuário criado com sucesso!")
    print("ID:", user.id)

if __name__ == "__main__":
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    create_user(name, email, password)
