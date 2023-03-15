
MAPPED_NUMS = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
}

def get_all_combinations(nums: str) -> list[str]:
    if not nums:
        return []
        
    def find_combos(symb_sets: list[str], curr_combo: str, result: list[str]) -> None:
        if len(symb_sets) == 0:
            result.append(curr_combo)
            return None
        for symbol in symb_sets[0]:
            curr_combo += symbol
            find_combos(symb_sets[1:], curr_combo, result)
            curr_combo = curr_combo[:-1]
        
    symbol_sets = [MAPPED_NUMS[i] for i in nums]
    find_combos(symbol_sets, "", result:=[])
    return result
