class TitleModifier:
    def __init__(self, base_title: str):
        """
        Initializes the TitleModifier with a base title.
        
        :param base_title: The original title of the application.
        """
        self.base_title = base_title

    def add_money_saver(self) -> str:
        """
        Modifies the base title to include 'Money Saver'
        
        :return: The updated title with 'Money Saver' included.
        """
        return f"{self.base_title} - Money Saver"


def test_title_modifier():
    # Test case 1: Standard title modification
    original_title = "Best Savings Tips"
    title_modifier = TitleModifier(original_title)
    updated_title = title_modifier.add_money_saver()
    assert updated_title == "Best Savings Tips - Money Saver", "Test Case 1 Failed"

    # Test case 2: Edge case with an empty string
    original_title_empty = ""
    title_modifier_empty = TitleModifier(original_title_empty)
    updated_title_empty = title_modifier_empty.add_money_saver()
    assert updated_title_empty == " - Money Saver", "Test Case 2 Failed"

    # Test case 3: Title with special characters
    original_title_special = "Savings $$$$"
    title_modifier_special = TitleModifier(original_title_special)
    updated_title_special = title_modifier_special.add_money_saver()
    assert updated_title_special == "Savings $$$$ - Money Saver", "Test Case 3 Failed"

    # Test case 4: Long title
    original_title_long = "This is a very long title meant to test the handling of title strings"
    title_modifier_long = TitleModifier(original_title_long)
    updated_title_long = title_modifier_long.add_money_saver()
    assert updated_title_long == "This is a very long title meant to test the handling of title strings - Money Saver", "Test Case 4 Failed"

    print("All test cases passed!")


if __name__ == "__main__":
    test_title_modifier()