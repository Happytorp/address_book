from sqlalchemy.orm import Session
from models import AddressModel
from schemas import AddressCreate, AddressUpdate


def create_address(db: Session, address: AddressCreate):
   """
   Create a new address record in the database.

   Args:
       db (Session): SQLAlchemy database session
       address (AddressCreate): Address data for creation

   Returns:
       AddressModel: The created address record
   """
   try:
       new_address = AddressModel(
           name=address.name,
           latitude=address.latitude,
           longitude=address.longitude
       )
       db.add(new_address)
       db.commit()
       db.refresh(new_address)
       return new_address
   except Exception as e:
       db.rollback()
       raise ValueError(f"Error creating address: {e}")


def get_address(db: Session, address_id: int):
   """
   Retrieve an address record by its ID.

   Args:
       db (Session): SQLAlchemy database session
       address_id (int): ID of the address to retrieve

   Returns:
       AddressModel: The retrieved address record
   """
   try:
       address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
       if not address:
           raise ValueError(f"Address with ID {address_id} not found")
       return address
   except Exception as e:
       raise ValueError(f"Error retrieving address: {e}")


def get_all_addresses(db: Session):
   """
   Retrieve all address records from the database.

   Args:
       db (Session): SQLAlchemy database session

   Returns:
       List[AddressModel]: List of all address records
   """
   try:
       addresses = db.query(AddressModel).all()
       return addresses
   except Exception as e:
       raise ValueError(f"Error retrieving addresses: {e}")

def update_address(db: Session, address_id: int, address_update: AddressUpdate):
   """
   Update an existing address record.

   Args:
       db (Session): SQLAlchemy database session
       address_id (int): ID of the address to update
       address_update (AddressUpdate): Updated address data

   Returns:
       AddressModel: The updated address record
   """
   try:
       address = get_address(db, address_id)
       address.name = address_update.name
       address.latitude = address_update.latitude
       address.longitude = address_update.longitude
       db.commit()
       db.refresh(address)
       return address
   except Exception as e:
       db.rollback()
       raise ValueError(f"Error updating address: {e}")


def delete_address(db: Session, address_id: int):
   """
   Delete an address record by its ID.

   Args:
       db (Session): SQLAlchemy database session
       address_id (int): ID of the address to delete

   Returns:
       None
   """
   try:
       address = get_address(db, address_id)
       db.delete(address)
       db.commit()
   except Exception as e:
       db.rollback()
       raise ValueError(f"Error deleting address: {e}")
