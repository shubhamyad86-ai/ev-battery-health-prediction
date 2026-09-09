"""
Utility Functions
"""

from pathlib import Path


def create_folder(folder):

    Path(folder).mkdir(
        parents=True,
        exist_ok=True
    )


def banner(title):

    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def separator():

    print("-" * 60)