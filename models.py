import os
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

Base = declarative_base()

class Employee(Base):
    """
    Table 1: employees [cite: 5]
    Personnel Information Table.
    """
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=False)
    rfid_tag = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Employee(name='{self.full_name}', role='{self.role}')>"


class InventoryItem(Base):
    """
    Table 2: inventory_items [cite: 9]
    Warehouse Inventory Table.
    """
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    last_updated_by = Column(String)
    last_update_rfid = Column(String)

    def __repr__(self):
        return f"<InventoryItem(name='{self.item_name}', qty={self.stock_quantity})>"


class VehicleMaintenanceLog(Base):
    """
    Table 3: vehicle_maintenance_logs [cite: 13]
    Fleet Maintenance Log.
    """
    __tablename__ = 'vehicle_maintenance_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_plate = Column(String, nullable=False)
    issue = Column(String, nullable=False)
    maintenance_date = Column(Date, nullable=False)
    technician_name = Column(String)
    technician_rfid = Column(String)
    def __repr__(self):
        return f"<MaintenanceLog(plate='{self.vehicle_plate}', date='{self.maintenance_date}')>"


# Database Connection Helper
def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set in .env file")
    return create_engine(db_url)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    """Helper to create tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()