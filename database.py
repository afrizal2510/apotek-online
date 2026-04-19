from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Alamat database dari Supabase (nanti kita isi lewat environment variable)
# Untuk sementara kita buat fleksibel
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./apotek_kita.db")

# Jika menggunakan PostgreSQL, kita perlu sedikit penyesuaian
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Obat(Base):
    __tablename__ = "data_obat"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String)
    stok = Column(Integer)
    satuan = Column(String)
    harga = Column(Integer)

Base.metadata.create_all(bind=engine)