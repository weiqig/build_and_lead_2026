from pathlib import Path
from email import policy
from email.parser import BytesParser


class Ingestor:
    '''
    Class used to perform data ingestion.
    Extracts and decodes job listings from provided
    seed 0_source/*.mhtml files into raw 1_bronze/*.html format.
    '''
    def __init__(self, process_amount: int | None = None):
        self.process_amount = process_amount
        self.extracted = 0
        self.failed = 0
        self.total = 0
        self.src_dir = Path("data/0_source")
        self.out_dir = Path("data/1_bronze")


    def ingest(self):
        print("week1 [week1] python main.py ingest")
        print("🥉 Bronze:...")

        if self.process_amount == 0:
            return

        for path in self.src_dir.glob("*.mhtml"):
            filename = path.stem
            content = self.extract_html(filename)

            if content:
                destination = self.out_dir / f"{filename}.html"
                if destination.exists():
                    print(f"{filename}.html already exists, proceeding...")
                else:
                    destination.write_text(content, encoding="utf-8")
                    self.extracted += 1
                    print(f"✅ Extracted: {filename}.mhtml")
            else:
                self.failed += 1
                print(f"⚠️ No HTML content found in: {filename}.mhtml")

            self.total += 1
            if self.total == self.process_amount:
                break

        print("")
        self.get_results()

    def extract_html(self, filename: str) -> str | None:
        '''
        Extracts html content from mhtml file if able.

        Arguments:
            filename: str - the file to be processed.
            ...
        '''
        path = Path(f"{self.src_dir}/{filename}.mhtml")
        if not path.exists():
            return None

        msg = BytesParser(policy=policy.default).parsebytes(path.read_bytes())

        for part in msg.walk():
            if part.get_content_type() == "text/html":
                content = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                return content.decode(charset, errors="replace")

    def get_results(self) -> None:
        '''
        Prints ingestion processing results.
        '''
        print("📊 Bronze Summary:")
        print(f"Total: {self.total} | Extracted: {self.extracted} | Failed: {self.failed}")

    def clean(self) -> None:
        '''
        Removes all files from specified folder.
        '''
        folder = Path(self.out_dir)

        if any(item.is_file() for item in folder.iterdir()):
            for item in folder.iterdir():
                if item.is_file():
                    item.unlink()
            print(f"Removed all files in {folder}.")
        else:
            print("Target folder is empty.")
            return