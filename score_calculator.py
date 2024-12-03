# score_calculator.py

from collections import Counter
from itertools import combinations

class ScoreCalculator:
    def __init__(self):
        pass

    def calculate_score(self, dice_values):
        # Sort dice values for consistency
        dice_values.sort()
        counts = Counter(dice_values)
        total_faces = sum(dice_values)

        # Check for special cases first
        special_score = self.check_special_cases(dice_values)
        if special_score is not None:
            return special_score

        num_ones = counts.get(1, 0)
        non_one_faces = [face for face in dice_values if face != 1]
        non_one_counts = Counter(non_one_faces)

        # Logic check order:

        # 1. 5 ① - 150 points
        if num_ones == 5:
            return 150

        # 2. 5 same - 100 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) + num_ones == 5:
                return 100 + total_faces

        # 3. 4 same, 1 ① - 90 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) + num_ones == 5 and num_ones == 1:
                if non_one_counts.get(face, 0) == 4:
                    return 90 + total_faces

        # 4. 4 same - 70 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 4:
                return 70 + total_faces

        # 5. 3 same, 2 ① - 80 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) + num_ones == 5 and num_ones == 2:
                if non_one_counts.get(face, 0) == 3:
                    return 80 + total_faces

        # 6. 3 same, 2 same (Full House) - 70 + sum_of_faces points
        if len(non_one_counts) == 2 and num_ones == 0:
            counts_list = list(non_one_counts.values())
            if sorted(counts_list) == [2, 3]:
                return 70 + total_faces

        # 7. 3 same, 1 ① - 65 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) + num_ones >= 4:
                if non_one_counts.get(face, 0) == 3 and num_ones == 1:
                    return 65 + total_faces

        # 8. 3 same - 40 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 3:
                return 40 + total_faces

        # 9. 2 same, 3 ① - 70 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 2 and num_ones == 3:
                return 70 + total_faces

        # 10. 2 same, 2 ① - 65 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 2 and num_ones == 2:
                return 65 + total_faces

        # 11. 2 same, 1 ① - 35 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 2 and num_ones == 1:
                return 35 + total_faces

        # 12. 2 same, 2 same - 40 + sum_of_faces points
        if len(non_one_counts) == 2 and num_ones == 0:
            counts_list = list(non_one_counts.values())
            if counts_list.count(2) == 2:
                return 40 + total_faces

        # 13. 2 same - 10 + sum_of_faces points
        for face in range(2, 7):
            if non_one_counts.get(face, 0) == 2:
                return 10 + total_faces

        # If no other combination is met, return sum of faces
        return total_faces

    def check_special_cases(self, dice_values):
        # Check for special cases
        # Since ① can be any number, check if we can form a straight using ① as needed

        # For ①②③④⑤ (130 points)
        # Need to check if dice contain 2,3,4,5 and ①s can fill in the missing numbers
        required_numbers = [2, 3, 4, 5]
        available_numbers = [face for face in dice_values if face != 1]
        num_ones = dice_values.count(1)

        missing_numbers = [num for num in required_numbers if num not in available_numbers]
        if len(missing_numbers) <= num_ones and max(dice_values) <= 5:
            return 130

        # For ②③④⑤⑥ (110 points)
        required_numbers = [2, 3, 4, 5, 6]
        missing_numbers = [num for num in required_numbers if num not in available_numbers]
        if len(missing_numbers) <= num_ones:
            return 110

        return None
