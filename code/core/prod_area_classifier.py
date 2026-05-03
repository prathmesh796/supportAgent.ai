import os
from pathlib import Path
from config import DATA_DIR

class ProductAreaExtractor:
    def __init__(self):
        self.areas_by_company = self._extract_product_areas()

    def _extract_product_areas(self):
        areas = {}
        if not DATA_DIR.exists():
            return areas
        
        for ecosystem in DATA_DIR.iterdir():
            if ecosystem.is_dir():
                company = ecosystem.name.lower()
                areas[company] = []
                for product_area in ecosystem.iterdir():
                    if product_area.is_dir():
                        # The normalized product area is the folder name
                        areas[company].append(product_area.name)
        return areas

    def get_valid_areas(self, company):
        company = str(company).lower()
        if company in self.areas_by_company:
            return self.areas_by_company[company]
        
        # fallback to all areas if company is not strictly matched or is None
        all_areas = set()
        for areas in self.areas_by_company.values():
            all_areas.update(areas)
        return list(all_areas)

product_area_extractor = ProductAreaExtractor()
