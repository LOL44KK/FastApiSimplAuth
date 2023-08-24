from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs,  AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


engine = create_async_engine("sqlite+aiosqlite:///users.db")

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[str]


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
   
    
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
async def get_session():
    async with async_session() as session:
        yield session


async def create_user(login, password):
    async with async_session() as session:
        user = User(login=login, password=password)
        session.add(user)
        await session.commit()


async def get_user(login):
    async with async_session() as session:
        stmt = select(User).where(User.login == login)
        user: User | None = await session.scalar(stmt)
        return user
        
            
async def check_user(userData):
    user = await get_user(userData.login)
    if user is not None:
        if userData.password == user.password:
            return True            
    return False