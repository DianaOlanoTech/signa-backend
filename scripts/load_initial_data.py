"""
Improved script for bulk loading initial data into the trademark database.
Run from backend directory: python scripts/load_initial_data_improved.py
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

# Configure Python path for imports
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

# Project imports
from sqlalchemy.orm import Session
from sqlalchemy import text
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
    },
    {
        "name": "Microsoft",
        "description": "Software and cloud computing services",
        "status": "Active"
    },
    {
        "name": "Amazon",
        "description": "E-commerce and cloud computing platform",
        "status": "Active"
    },
    {
        "name": "Samsung",
        "description": "Electronics and semiconductor manufacturer",
        "status": "Active"
    },
    {
        "name": "Toyota",
        "description": "Automotive manufacturer",
        "status": "Active"
    },
    {
        "name": "Visa",
        "description": "Payment technology company",
        "status": "Active"
    },
    {
        "name": "IBM",
        "description": "Technology and consulting services",
        "status": "Active"
    },
    {
        "name": "Intel",
        "description": "Semiconductor chip manufacturer",
        "status": "Active"
    },
    {
        "name": "Disney",
        "description": "Entertainment and media conglomerate",
        "status": "Active"
    },
    {
        "name": "BMW",
        "description": "Luxury automotive manufacturer",
        "status": "Active"
    }
]

# Additional test data for different statuses
ADDITIONAL_TEST_DATA = [
    {
        "name": "Blockbuster",
        "description": "Former video rental company",
        "status": "Expired"
    },
    {
        "name": "NewBrand2024",
        "description": "New trademark application pending approval",
        "status": "Pending"
    },
    {
        "name": "OldTech",
        "description": "Discontinued technology brand",
        "status": "Inactive"
    }
]


class BulkDataLoader:
    """Class to handle bulk data loading operations."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.db: Session = SessionLocal()
        self.validate_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def validate_connection(self):
        """Validate database connection and show environment info"""
        try:
            print(f"🔧 Environment: {settings.ENVIRONMENT}")
            print(f"🔧 Database type: {'PostgreSQL' if settings.is_postgres else 'SQLite'}")

            is_production = settings.ENVIRONMENT == "production"
            print(f"🔧 Production deployment: {is_production}")

            if self.verbose:
                print(f"🔧 Database URL: {settings.DATABASE_URL}")

            # Test connection
            if settings.is_sqlite:
                self.db.execute(text("SELECT 1"))
            else:
                self.db.execute(text("SELECT 1"))  # A simple SELECT 1 works for both

            print("✅ Database connection successful")

        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise

    def ensure_tables_exist(self):
        """Ensure all tables exist"""
        try:
            print("🏗️ Creating tables if they don't exist...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tables are ready")
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise

    def clear_existing_data(self):
        """Clear existing data (optional)."""
        try:
            print("🗑️ Clearing existing data...")
            count = self.db.query(Trademark).count()
            if count > 0:
                self.db.query(Trademark).delete()
                self.db.commit()
                print(f"✅ Cleared {count} existing records")
            else:
                print("ℹ️ No existing data to clear")
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            self.db.rollback()
            raise

    def load_from_list(self, data: List[Dict[str, Any]], skip_existing: bool = True) -> int:
        """Load data from a list of dictionaries."""
        print(f"📥 Loading {len(data)} records from list...")
        loaded_count = 0
        skipped_count = 0
        error_count = 0

        for item in data:
            try:
                # Check if trademark already exists
                existing = self.db.query(Trademark).filter(
                    Trademark.name == item['name']
                ).first()

                if existing and skip_existing:
                    skipped_count += 1
                    if self.verbose:
                        print(f"  ⚠️ Skipped (already exists): {item['name']}")
                    continue
                elif existing and not skip_existing:
                    # Update existing record
                    for key, value in item.items():
                        setattr(existing, key, value)
                    self.db.commit()
                    loaded_count += 1
                    if self.verbose:
                        print(f"  🔄 Updated: {item['name']}")
                    continue

                # Create new trademark
                trademark_data = TrademarkCreate(**item)
                crud_trademark.create_trademark(db=self.db, trademark=trademark_data)
                loaded_count += 1
                if self.verbose:
                    print(f"  ✅ Loaded: {item['name']}")

            except Exception as e:
                error_count += 1
                print(f"  ❌ Error loading {item.get('name', 'Unknown')}: {e}")
                # Don't break the entire process for one error
                continue

        print(f"📊 Summary: {loaded_count} loaded, {skipped_count} skipped, {error_count} errors")
        return loaded_count

    def get_current_stats(self):
        """Get current database statistics."""
        try:
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

        except Exception as e:
            print(f"❌ Error getting statistics: {e}")

    def show_sample_data(self, limit: int = 5):
        """Show sample data from the database"""
        try:
            print(f"\n📋 SAMPLE DATA (first {limit} records):")
            trademarks = self.db.query(Trademark).limit(limit).all()

            if not trademarks:
                print("  No data found")
                return

            for tm in trademarks:
                desc = tm.description[:50] + "..." if tm.description and len(tm.description) > 50 else tm.description
                print(f"  ID: {tm.id:2d} | {tm.name:15s} | {tm.status:10s} | {desc or 'No description'}")

        except Exception as e:
            print(f"❌ Error showing sample data: {e}")


def main():
    """Main function of the script."""
    parser = argparse.ArgumentParser(description="Load initial data into trademark database")
    parser.add_argument("--clear", action="store_true", help="Clear existing data before loading")
    parser.add_argument("--minimal", action="store_true", help="Load only basic sample data")
    parser.add_argument("--update-existing", action="store_true", help="Update existing records instead of skipping")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--show-sample", action="store_true", help="Show sample data after loading")

    args = parser.parse_args()

    print("🚀 STARTING BULK DATA LOADING")
    print("=" * 50)

    try:
        with BulkDataLoader(verbose=args.verbose) as loader:
            # Ensure tables exist
            loader.ensure_tables_exist()

            # Show initial statistics
            print("\n📊 INITIAL STATISTICS:")
            loader.get_current_stats()

            # Clear existing data if requested
            if args.clear:
                loader.clear_existing_data()

            # Prepare data to load
            data_to_load = SAMPLE_TRADEMARKS.copy()
            if not args.minimal:
                data_to_load.extend(ADDITIONAL_TEST_DATA)

            # Load data
            print(f"\n📥 LOADING DATA")
            print("-" * 30)
            total_loaded = loader.load_from_list(
                data_to_load,
                skip_existing=not args.update_existing
            )

            # Show final statistics
            print("\n📊 FINAL STATISTICS:")
            loader.get_current_stats()

            # Show sample data if requested
            if args.show_sample:
                loader.show_sample_data()

            print(f"\n✅ PROCESS COMPLETED")
            print("=" * 50)
            print(f"Records processed: {total_loaded}")

    except Exception as e:
        print(f"\n❌ PROCESS FAILED: {e}")
        if args.verbose:
            import traceback
            print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()