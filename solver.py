"""
CSC148, Winter 2021
Assignment 2: Automatic Puzzle Solver
==============================
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jonathan Calver, Sophia Huynh,
         Maryam Majedi, and Jaisie Sin.

All of the files in this directory are:
Copyright (c) 2021 Diane Horton, Jonathan Calver, Sophia Huynh,
                   Maryam Majedi, and Jaisie Sin.

=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


def _path_finder(path: List, puzzle: Puzzle) -> Optional:
    """To remove the extra layer looping """
    if path:
        return [puzzle] + path
    else:
        return None


class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        stack_lst_1 = []

        # If the value of seen in none, replace with an empty list
        if seen is None:
            seen = set()
        # If the puzzle is not solvable, return empty list
        if puzzle.fail_fast() is True:
            return stack_lst_1
        elif puzzle.is_solved() is True:
            stack_lst_1.append(puzzle)
            return stack_lst_1
        else:
            # For the puzzle that is solvable, append it to the path.
            stack_lst_1.append(puzzle)
            seen.add(puzzle.__str__())
            # Create new list with extensions of the puzzle.
            extension_lst = puzzle.extensions()
            # For each extension, check if it solvable(fail.fast = False),
            # and not in seen).
            # If true, append to stack_lst. Recurse it over every updated puzzle
            # Else, append to seen.
            # for upd_puzzle in extension_lst:
            #     if upd_puzzle.fail_fast() is False \
            #             and upd_puzzle.__str__() not in seen:
            #         seen.add(upd_puzzle.__str__())
            #         path = self.solve(upd_puzzle, seen)
            #         result = _nester_helper(path, puzzle,
            #         stack_lst_1, upd_puzzle)[0]
            #         stack_lst_1 = _nester_helper(path,
            #         puzzle, stack_lst_1, upd_puzzle)[1]
            #         return result
            #         # if path:
            #         #     if path[-1].is_solved():
            #         #         stack_lst_1.append(upd_puzzle)
            #         #         return _path_finder(path, puzzle)
            #         #         # return self._path_finder(path, puzzle)
            #     else:
            #         seen.add(upd_puzzle.__str__())
            helper = self._helper_function(puzzle, extension_lst,
                                           seen, stack_lst_1)
            if helper:
                return helper
        return helper

    def _helper_function(self, puzzle: Puzzle, extension_lst: list, seen: set,
                         stack_lst_1: list) -> Optional[List]:
        """Helper function"""
        for upd_puzzle in extension_lst:
            if upd_puzzle.fail_fast() is False \
                    and upd_puzzle.__str__() not in seen:
                seen.add(upd_puzzle.__str__())
                path = self.solve(upd_puzzle, seen)
                if path and path[-1].is_solved():
                    stack_lst_1.append(upd_puzzle)
                    return _path_finder(path, puzzle)
            else:
                seen.add(upd_puzzle.__str__())
        return []


class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """

        if puzzle.fail_fast() is True:
            return []

        # check that its solved!
        if puzzle.is_solved():
            return [puzzle]

        # create empty set
        if seen is None:
            seen = set(puzzle.__str__())

        # at this point we know its solvable so we may proceed
        # get extensions
        puzzle_extensions = puzzle.extensions()

        # create queue
        puzzle_queue = Queue()

        # now we can populate the queue
        for extension in puzzle_extensions:
            # recall that seen is a set of *string representations*
            if extension.__str__() not in seen:
                puzzle_queue.enqueue([puzzle, extension])
                seen.add(extension.__str__())

        # now that queue is populated with the [puzzle, extension] we loop
        while not puzzle_queue.is_empty():
            # get the path to be tested
            test_path = puzzle_queue.dequeue()
            # print(test_path)
            # get the state to be tested
            test_path_state = test_path[-1]

            # check that test path is not solved
            if test_path_state.is_solved():
                return test_path

            if not test_path_state.fail_fast():
                # get extensions
                test_extensions = test_path_state.extensions()
                # for extension in test_extensions:
                #     if extension.__str__() not in seen:
                #         # we yeet a new updated path in the queue
                #         new_path = test_path.copy() + [extension]
                #         # new_path.append(extension)
                #         puzzle_queue.enqueue(new_path)
                #         seen.add(extension.__str__)
                # self._solve_helper(test_path, puzzle_queue, seen)
                _helper_extension_loop(test_extensions, test_path, seen,
                                       puzzle_queue)
        # if this loop never returns a solved test path
        return []


def _helper_extension_loop(test_extensions: List[Puzzle],
                           test_path: List[Puzzle], seen: Set[str],
                           puzzle_queue: Queue) -> None:
    """ Helper function for solve BFS. This goes through the list
    test_extensions and adds it into puzzle_queue and seen if this particular
     extension is not in seen. Seen and Puzzle Queue may be mutated.
    """
    for extension in test_extensions:
        if extension.__str__() not in seen:
            new_path = test_path.copy() + [extension]
            # new_path.append(extension)
            puzzle_queue.enqueue(new_path)
            seen.add(extension.__str__)


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
