from unittest.mock import patch
import item26_good
from item26_good import call_print_deco, print_deco


if __name__ == "__main__":
    with patch(f"{item26_good.__name__}.{print_deco.__name__}") as mocked:
        mocked.side_effect = lambda : print("mocked!!")

        call_print_deco()
