# score_calculator.py

from collections import Counter

class ScoreCalculator:
    def __init__(self):
        pass

    def calculate_score(self, dice_values):
        # Sort dice values for consistency
        dice_values.sort()
        counts = Counter(dice_values)
        total_faces = sum(dice_values)

        # Check for special cases first (do not use ones as wildcards here)
        special_score = self.check_special_cases(dice_values)
        if special_score is not None:
            return special_score

        num_ones = counts.get(1, 0)
        # Exclude ones for non-one counts
        non_one_counts = Counter({face: count for face, count in counts.items() if face != 1})

        # Adjusted counts with ones acting as wildcards
        adjusted_counts = {}
        for face in range(2, 7):
            adjusted_counts[face] = counts.get(face, 0) + num_ones

        # Now check for combinations using adjusted counts

        # 1. 5 same (including ones as wildcards) - 100 + sum_of_faces points
        for face in range(2, 7):
            if adjusted_counts[face] >= 5:
                return 100 + total_faces

        # 2. 4 same (including ones as wildcards) - 70 + sum_of_faces points
        for face in range(2, 7):
            if adjusted_counts[face] >= 4:
                return 70 + total_faces

        # 3. Full House (3 same and 2 same) - 70 + sum_of_faces points
        for three_face in range(2, 7):
            if adjusted_counts[three_face] >= 3:
                remaining_ones = num_ones - max(0, 3 - counts.get(three_face, 0))
                for two_face in range(2, 7):
                    if two_face != three_face:
                        adjusted_two_count = counts.get(two_face, 0) + remaining_ones
                        if adjusted_two_count >= 2:
                            return 70 + total_faces

        # 4. 3 same (including ones as wildcards) - 40 + sum_of_faces points
        for face in range(2, 7):
            if adjusted_counts[face] >= 3:
                return 40 + total_faces

        # 5. Two Pairs (including ones as wildcards) - 40 + sum_of_faces points
        pair_count = 0
        for face in range(2, 7):
            if adjusted_counts[face] >= 2:
                pair_count += 1
        if pair_count >= 2:
            return 40 + total_faces

        # 6. One Pair (including ones as wildcards) - 10 + sum_of_faces points
        for face in range(2, 7):
            if adjusted_counts[face] >= 2:
                return 10 + total_faces

        # If no other combination is met, return sum of faces
        return total_faces

    def check_special_cases(self, dice_values):
        # Check for special cases without using ones as wildcards

        # Check for 1-2-3-4-5 straight (130 points)
        if set(dice_values) == {1, 2, 3, 4, 5}:
            return 130

        # Check for 2-3-4-5-6 straight (110 points)
        if set(dice_values) == {2, 3, 4, 5, 6}:
            return 110

        return None
