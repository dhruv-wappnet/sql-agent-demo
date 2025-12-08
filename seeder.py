import datetime
import random
from sqlalchemy.orm import sessionmaker
from models import get_engine, init_db, Employee, InventoryItem, VehicleMaintenanceLog

def seed_data():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Clear existing data to avoid duplicates on re-run
    session.query(VehicleMaintenanceLog).delete()
    session.query(InventoryItem).delete()
    session.query(Employee).delete()
    print("Existing data cleared.")

    # ---------------------------------------------------------
    # SEED TABLE 1: Employees
    # ---------------------------------------------------------
    employees_data = [
        {"full_name": "Alice Carter", "role": "Logistics Coordinator", "department": "Logistics", "rfid_tag": "RFID-001"},
        {"full_name": "Bob Smith", "role": "Technician", "department": "Maintenance", "rfid_tag": "RFID-002"},
        {"full_name": "Charlie Davis", "role": "Warehouse Manager", "department": "Warehouse", "rfid_tag": "RFID-003"},
        {"full_name": "Diana Evans", "role": "Driver", "department": "Logistics", "rfid_tag": "RFID-004"},
        {"full_name": "Ethan Foster", "role": "Technician", "department": "Maintenance", "rfid_tag": "RFID-005"},
        {"full_name": "Fiona Green", "role": "HR Specialist", "department": "HR", "rfid_tag": "RFID-006"},
        {"full_name": "George Harris", "role": "Warehouse Staff", "department": "Warehouse", "rfid_tag": "RFID-007"},
        {"full_name": "Hannah White", "role": "Logistics Manager", "department": "Logistics", "rfid_tag": "RFID-008"},
        {"full_name": "Ian Black", "role": "Technician", "department": "Maintenance", "rfid_tag": "RFID-009"},
        {"full_name": "Julia Roberts", "role": "Driver", "department": "Logistics", "rfid_tag": "RFID-010"},
    ]

    employees = [Employee(**data) for data in employees_data]
    session.add_all(employees)
    session.commit()
    print(f"{len(employees)} Employees seeded.")

    # ---------------------------------------------------------
    # SEED TABLE 2: Inventory Items
    # ---------------------------------------------------------
    inventory_data = [
        {"item_name": "Cordless Drill 18V", "stock_quantity": 15, "last_updated_by": "Bob Smith", "last_update_rfid": "RFID-002"},
        {"item_name": "Safety Gloves", "stock_quantity": 200, "last_updated_by": "Charlie Davis", "last_update_rfid": "RFID-003"},
        {"item_name": "Torque Wrench", "stock_quantity": 5, "last_updated_by": "Alice Carter", "last_update_rfid": "RFID-001"},
        {"item_name": "Hammer", "stock_quantity": 50, "last_updated_by": "George Harris", "last_update_rfid": "RFID-007"},
        {"item_name": "Screwdriver Set", "stock_quantity": 100, "last_updated_by": "Charlie Davis", "last_update_rfid": "RFID-003"},
        {"item_name": "LED Work Light", "stock_quantity": 8, "last_updated_by": "Bob Smith", "last_update_rfid": "RFID-002"},
        {"item_name": "Hydraulic Jack", "stock_quantity": 12, "last_updated_by": "Ethan Foster", "last_update_rfid": "RFID-005"},
        {"item_name": "Brake Pads", "stock_quantity": 40, "last_updated_by": "Ian Black", "last_update_rfid": "RFID-009"},
        {"item_name": "Oil Filter", "stock_quantity": 60, "last_updated_by": "Bob Smith", "last_update_rfid": "RFID-002"},
        {"item_name": "Air Filter", "stock_quantity": 35, "last_updated_by": "Ethan Foster", "last_update_rfid": "RFID-005"},
        {"item_name": "Spark Plugs", "stock_quantity": 150, "last_updated_by": "Ian Black", "last_update_rfid": "RFID-009"},
        {"item_name": "Tire Pressure Gauge", "stock_quantity": 25, "last_updated_by": "George Harris", "last_update_rfid": "RFID-007"},
    ]

    inventory_items = [InventoryItem(**data) for data in inventory_data]
    session.add_all(inventory_items)
    session.commit()
    print(f"{len(inventory_items)} Inventory Items seeded.")

    # ---------------------------------------------------------
    # SEED TABLE 3: Vehicle Maintenance Logs
    # ---------------------------------------------------------
    today = datetime.date.today()
    
    maintenance_logs_data = [
        {"vehicle_plate": "GJ-01-AB-1234", "issue": "Brake pads replacement", "maintenance_date": today - datetime.timedelta(days=3), "technician_name": "Bob Smith", "technician_rfid": "RFID-002"},
        {"vehicle_plate": "MH-12-XY-9876", "issue": "Oil Change", "maintenance_date": today - datetime.timedelta(days=14), "technician_name": "Bob Smith", "technician_rfid": "RFID-002"},
        {"vehicle_plate": "DL-04-ZZ-5555", "issue": "Engine tuning", "maintenance_date": today, "technician_name": "David Miller", "technician_rfid": "RFID-999"}, # Ghost employee
        {"vehicle_plate": "KA-05-CC-1111", "issue": "Tire rotation", "maintenance_date": today - datetime.timedelta(days=1), "technician_name": "Ethan Foster", "technician_rfid": "RFID-005"},
        {"vehicle_plate": "TN-09-DD-2222", "issue": "Battery replacement", "maintenance_date": today - datetime.timedelta(days=5), "technician_name": "Ian Black", "technician_rfid": "RFID-009"},
        {"vehicle_plate": "GJ-01-AB-1234", "issue": "General Service", "maintenance_date": today - datetime.timedelta(days=30), "technician_name": "Bob Smith", "technician_rfid": "RFID-002"},
        {"vehicle_plate": "MH-12-XY-9876", "issue": "Coolant leak fix", "maintenance_date": today - datetime.timedelta(days=2), "technician_name": "Ethan Foster", "technician_rfid": "RFID-005"},
        {"vehicle_plate": "UP-14-EE-3333", "issue": "Transmission check", "maintenance_date": today - datetime.timedelta(days=6), "technician_name": "Ian Black", "technician_rfid": "RFID-009"},
        {"vehicle_plate": "WB-10-FF-4444", "issue": "Headlight replacement", "maintenance_date": today - datetime.timedelta(days=10), "technician_name": "Bob Smith", "technician_rfid": "RFID-002"},
        {"vehicle_plate": "KA-05-CC-1111", "issue": "Wiper blade replacement", "maintenance_date": today - datetime.timedelta(days=20), "technician_name": "Ethan Foster", "technician_rfid": "RFID-005"},
    ]

    maintenance_logs = [VehicleMaintenanceLog(**data) for data in maintenance_logs_data]
    session.add_all(maintenance_logs)
    session.commit()
    print(f"{len(maintenance_logs)} Vehicle Maintenance Logs seeded.")
    
    print("--- Database Seeding Complete ---")

if __name__ == "__main__":
    # Ensure tables exist first
    init_db()
    # Run seeder
    seed_data()
plete ---")

if __name__ == "__main__":
    # Ensure tables exist first
    init_db()
    # Run seeder
    seed_data()plete ---")

if __name__ == "__main__":
    # Ensure tables exist first
    init_db()
    # Run seeder
    seed_data()