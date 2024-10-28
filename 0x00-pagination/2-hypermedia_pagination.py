#!/usr/bin/env python3
"""Helper function for pagination."""

from typing import Tuple, List, Dict
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    "Gets the index range for a specific page and page size."
    startIndex = (page - 1) * page_size
    endIndex = startIndex + page_size
    return (startIndex, endIndex)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        "Fetches a single page of data"
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        startIndex, endIndex = index_range(page, page_size)
        data = self.dataset()
        return data[startIndex:endIndex] if startIndex < len(data) else []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """إرجاع قاموس يحتوي على معلومات الصفحة."""
        data = self.get_page(page, page_size)
        pagesTotal = math.ceil(len(self.dataset()) / page_size)

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if page < pagesTotal else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': pagesTotal
        }
