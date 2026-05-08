from pathlib import Path
from pydantic import BaseModel, Field, model_validator, ValidationInfo, ValidationError
from bs4 import BeautifulSoup
from typing_extensions import Self


class Processor:

    class JobListing(BaseModel):
        source_id: str | None = Field(description="Original URL found in the HTML metadata")
        job_title: str | None
        description: str | None
        company: str | None

        @model_validator(mode="after")
        def validate_fields(self, info: ValidationInfo) -> Self:
            filename = info.context.get("filename")
            missing = []

            if not self.source_id:
                missing.append("source_id")
            if not self.job_title:
                missing.append("job_title")
            if not self.description:
                missing.append("description")
            if not self.company:
                missing.append("company")

            if missing:
                raise ValueError(f"⚠️  Missing {', '.join(missing)} in: {filename}.html")

            return self

    def __init__(self):
        self.processed = 0
        self.skipped = 0
        self.total = 0
        self.src_dir = Path("data/1_bronze")
        self.out_dir = Path("data/2_silver")

    def process(self):
        print("(week_1) week_1 [week1] python main.py process")
        print("🥈 Silver:...")

        for path in self.src_dir.glob("*.html"):
            filename = path.stem
            html = path.read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            try:
                source_id = self.extract_source_id(soup)
                job_title = self.extract_job_title(soup)
                company = self.extract_company(soup)
                description = self.extract_description(soup)
                data = {
                        'source_id': source_id,
                        'job_title': job_title,
                        'company': company,
                        'description': description
                    }
                job = self.JobListing.model_validate(
                    data,
                    context={"filename": filename}
                )
                destination = self.out_dir / f"{filename}.json"
                with destination.open("w", encoding="utf-8") as f:
                    f.write(job.model_dump_json(indent=2))
                print(f"✅ Processed: {filename}.html")
                self.processed += 1
            except ValidationError as e:
                msg = e.errors()[0].get("ctx", {}).get("error")
                print(msg)
                self.skipped += 1
            except Exception as e:
                print(e)
                self.skipped += 1
                continue
            self.total += 1

        print("")
        self.get_results()

    def get_results(self) -> None:
        '''
        Prints ingestion processing results.
        '''
        print("📊 Silver Summary:")
        print(f"Total: {self.total} | Processed: {self.processed} | Skipped: {self.skipped}")


    def extract_source_id(self, soup: BeautifulSoup) -> str | None:

        meta = soup.find("meta", attrs={"property": "og:url"})
        if meta and meta.get("content"):
            return meta["content"].split("/")[-1]

        return None


    def extract_job_title(self, soup: BeautifulSoup) -> str | None:

        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        title = soup.find(attrs={"data-automation": "job-detail-title"})
        if title:
            return title.get_text(strip=True)

        return None


    def extract_company(self, soup: BeautifulSoup) -> str | None:

        company = soup.find(attrs={"data-automation": "advertiser-name"})
        if company:
            return company.get_text(strip=True)

        meta = soup.find("meta", attrs={"name": "author"})
        if meta and meta.get("content"):
            return meta["content"]

        return None


    def extract_description(self, soup: BeautifulSoup) -> str | None:

        description = soup.find(attrs={"data-automation": "jobAdDetails"})
        if description:
            return description.get_text(strip=True)

        return None

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
