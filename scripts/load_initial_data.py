"""
Script for bulk loading initial data into the trademark database.
Run from backend directory: python scripts/load_initial_data.py
"""

import sys
from pathlib import Path
from typing import List, Dict, Any

# Configure Python path for imports
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

# Project imports
from sqlalchemy.orm import Session
from src.db.session import SessionLocal, engine
from src.db.base import Base, Trademark
from src.crud import crud_trademark
from src.api.v1.schemas.trademarks import TrademarkCreate

# Import settings after configuring the path
from src.core.config import settings

# Sample data to load
SAMPLE_TRADEMARKS = [
    {
        "name": "Nike",
        "description": "International sports brand known for footwear and athletic apparel",
        "status": "Active"
    },
    {
        "name": "Apple",
        "description": "Technology company specialized in consumer electronics",
        "status": "Active"
    },
    {
        "name": "Coca-Cola",
        "description": "Globally recognized soft drink brand",
        "status": "Active"
    },
    {
        "name": "McDonald's",
        "description": "Fast food restaurant chain",
        "status": "Active"
    },
    {
        "name": "Google",
        "description": "Search engine and technology services",
        "status": "Active"
    },
    {
        "name": "Starbucks",
        "description": "International coffeehouse chain",
        "status": "Active"
    }
]


class BulkDataLoader:
    """Class to handle bulk data loading operations."""

    def __init__(self):
        self.db: Session = SessionLocal()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def clear_existing_data(self):
        """Clear existing data (optional)."""
        print("🗑️ Clearing existing data...")
        self.db.query(Trademark).delete()
        self.db.commit()
        print("✅ Existing data cleared")

    def load_from_list(self, data: List[Dict[str, Any]]) -> int:
        """Load data from a list of dictionaries."""
        print(f"📥 Loading {len(data)} records from list...")
        loaded_count = 0

        for item in data:
            try:
                trademark_data = TrademarkCreate(**item)
                crud_trademark.create_trademark(db=self.db, trademark=trademark_data)
                loaded_count += 1
                print(f"  ✅ Loaded: {item['name']}")
            except Exception as e:
                print(f"  ❌ Error loading {item.get('name', 'Unknown')}: {e}")

        print(f"📊 Total records loaded: {loaded_count}/{len(data)}")
        return loaded_count

    def get_current_stats(self):
        """Get current database statistics."""
        total = self.db.query(Trademark).count()
        active = self.db.query(Trademark).filter(Trademark.status == "Active").count()
        inactive = self.db.query(Trademark).filter(Trademark.status == "Inactive").count()
        pending = self.db.query(Trademark).filter(Trademark.status == "Pending").count()
        expired = self.db.query(Trademark).filter(Trademark.status == "Expired").count()

        print("\n📊 CURRENT STATISTICS:")
        print(f"  Total trademarks: {total}")
        print(f"  Active: {active}")
        print(f"  Inactive: {inactive}")
        print(f"  Pending: {pending}")
        print(f"  Expired: {expired}")


def main():
    """Main function of the script."""
    print("🚀 STARTING BULK DATA LOADING")
    print("=" * 50)

    with BulkDataLoader() as loader:

        # Show initial statistics
        print("\n📊 INITIAL STATISTICS:")
        loader.get_current_stats()

        # Ask if user wants to clear existing data
        if input("\nDo you want to clear existing data? (y/N): ").lower().strip() == 'y':
            loader.clear_existing_data()

        # Load sample data
        print(f"\n📥 LOADING SAMPLE DATA")
        print("-" * 30)
        total_loaded = loader.load_from_list(SAMPLE_TRADEMARKS)

        # Show final statistics
        print("\n📊 FINAL STATISTICS:")
        loader.get_current_stats()

        print(f"\n✅ PROCESS COMPLETED")
        print("=" * 50)
        print(f"Records loaded: {total_loaded}")


if __name__ == "__main__":
    # The argument parsing logic remains the same.
    main()