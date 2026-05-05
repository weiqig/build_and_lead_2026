import json
import sqlite3
from pathlib import Path

class Loader:
    ...
    def __init__(self):
        self.inserted = 0
        self.skipped = 0
        self.total = 0
        self.src_dir: Path = Path("data/2_silver")
        self.database: Path = Path("data/3_gold/jobs.db")
        self.db = None

    def load(self):
        self.initialize()
        print("(week_1) week_1 [week1●] python main.py load")
        print("🥇 Gold:...")
        try:
            # self.delete_data()
            self.insert_silver_data()
        except Exception as e:
            print(e)
        print("")
        self.get_results()

    def initialize(self):
        '''
        Initialize and create the database if it doesn't exist.
        '''
        if self.database.exists():
            pass
        else:
            with open(self.database, 'w') as new_file:
                pass
        self.db = sqlite3.connect(self.database)
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS JOBS(
            source_id TEXT PRIMARY KEY,
            job_title TEXT,
            company TEXT,
            description TEXT,
            tech_stack TEXT
        )
        """)
        self.db.commit()

    def insert_silver_data(self) -> None:
        '''
            Insert json data into the database.
        '''
        files = sorted([f for f in self.src_dir.iterdir()])
        for file in files:
            filename = f"{file.stem}.json"
            path = Path(file)
            silver_data = json.loads(path.read_text(encoding="utf-8"))
            fields, gold_data = list(silver_data.keys()), list(silver_data.values())
            query = f"""
                        INSERT OR IGNORE INTO JOBS (
                                {', '.join(fields)}
                            )
                            VALUES(
                                {', '.join(['?'] * len(fields))}
                            )
                    """
            if self.db.execute(query, gold_data).rowcount == 0:
                print("⏭️ Skipped (duplicate):", filename)
                self.skipped += 1
            else:
                print("✅ Inserted:", filename)
                self.inserted += 1
            self.total += 1
        self.db.commit()
        self.db.close()

    def delete_data(self) -> None:
        '''
        Drop and delete the JOBS table.
        '''
        if self.db is None:
            self.db = sqlite3.connect(self.database)
        self.db.execute("DELETE FROM JOBS")
        self.db.commit()
        print("Deleted all data from JOBS table.")

    def get_results(self) -> None:
        '''
        Prints loader processing results.
        '''
        print("📊 Gold Summary:")
        print(f"Total: {self.total} | Inserted: {self.inserted} | Skipped: {self.skipped}")