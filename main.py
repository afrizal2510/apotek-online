from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Penting untuk Frontend
from sqlalchemy.orm import Session
import database

app = FastAPI()

# --- BAGIAN 1: IZIN AKSES FRONTEND (CORS) ---
# Ini agar file index.html bisa membaca data dari server ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fungsi untuk koneksi database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- BAGIAN 2: PERINTAH-PERINTAH (ENDPOINTS) ---

@app.get("/")
def home():
    return {"pesan": "Server Apotek Database Aktif!"}

# Lihat Semua Obat
@app.get("/stok-asli")
def lihat_stok(db: Session = Depends(get_db)):
    return db.query(database.Obat).all()

# Tambah Obat Baru
@app.post("/tambah-obat")
def tambah_obat(nama: str, stok: int, satuan: str, harga: int, db: Session = Depends(get_db)):
    obat_baru = database.Obat(nama=nama, stok=stok, satuan=satuan, harga=harga)
    db.add(obat_baru)
    db.commit()
    return {"status": "Berhasil simpan ke database!"}

# Cari obat berdasarkan nama
@app.get("/cari-obat")
def cari_obat(nama: str, db: Session = Depends(get_db)):
    hasil = db.query(database.Obat).filter(database.Obat.nama.contains(nama)).all()
    return hasil

# Update Stok Obat
@app.put("/update-stok")
def update_stok(id_obat: int, jumlah_baru: int, db: Session = Depends(get_db)):
    obat = db.query(database.Obat).filter(database.Obat.id == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    obat.stok = jumlah_baru
    db.commit()
    return {"status": "Stok diperbarui!"}

# Hapus Obat (Perintah yang Anda tanyakan)
@app.delete("/hapus-obat/{id_obat}")
def hapus_obat(id_obat: int, db: Session = Depends(get_db)):
    obat = db.query(database.Obat).filter(database.Obat.id == id_obat).first()
    if not obat:
        raise HTTPException(status_code=404, detail="Obat tidak ditemukan")
    db.delete(obat)
    db.commit()
    return {"status": f"Obat {obat.nama} berhasil dihapus!"}