import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            domain = self.domains[var].copy()
            for word in domain:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        domain = self.domains[x].copy()
        for word in domain:
            same = 0
            for word2 in self.domains[y]:
                if word != word2:
                    break
                same += 1
            if same == len(self.domains[y]):
                self.domains[x].remove(word)
                revised = True
                continue
            if y in self.crossword.neighbors(x):
                overlap = self.crossword.overlaps[x, y]
                no_overlap = 0
                for word2 in self.domains[y]:
                    if word[overlap[0]] == word2[overlap[1]]:
                        break
                    no_overlap += 1
                if no_overlap == len(self.domains[y]):
                    self.domains[x].remove(word)
                    revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list()
            for var1 in self.crossword.variables:
                for var2 in self.crossword.variables:
                    if var1 != var2:
                        arcs.append((var1, var2))

        while len(arcs) != 0:
            arc = arcs.pop()
            if self.revise(arc[0], arc[1]):
                if self.domains[arc[0]] == 0:
                    return False
                for var in self.crossword.neighbors(arc[0]):
                    arcs.append((arc[0], var))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True

        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var1 in assignment:
            for var2 in assignment:
                if var1 == var2:
                    continue
                elif assignment[var1] == assignment[var2]:
                    return False

        for var in assignment:
            if len(assignment[var]) != var.length:
                return False

        for var in assignment:
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment.keys():
                    overlap = self.crossword.overlaps[(var, neighbor)]
                    if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domains = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        copy = neighbors.copy()
        for neighbor in copy:
            if neighbor in assignment.keys():
                neighbors.remove(neighbor)

        n = dict()
        for word in domains:
            n[word] = 0
            for neighbor in neighbors:
                for word2 in self.domains[neighbor]:
                    if word == word2:
                        n[word] += 1
                        continue
                    overlap = self.crossword.overlaps[(var, neighbor)]
                    if word[overlap[0]] != word2[overlap[1]]:
                        n[word] += 1

        sorted_n = {k: v for k, v in sorted(n.items(), key=lambda item: item[1])}

        return list(sorted_n.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # all unassigned vars
        unassigned = list()
        for var in self.crossword.variables:
            if var not in assignment.keys():
                unassigned.append(var)

        # every var with number of values reaming
        reaming = dict()
        for var in unassigned:
            reaming[var] = len(self.domains[var])

        # sort the vars by MRV
        sorted_reaming = {k: v for k, v in sorted(reaming.items(), key=lambda item: item[1])}
        unassigned = list(sorted_reaming.keys())

        # only the vars with minimum number of values
        fewest = sorted_reaming[unassigned[0]]
        mrv = list()
        for var in unassigned:
            if sorted_reaming[var] == fewest:
                mrv.append(var)

        if len(mrv) == 1:
            return mrv[0]

        # degree

        neighbors = dict()
        for var in mrv:
            neighbors[var] = len(self.crossword.neighbors(var))

        sorted_neighbors = {k: v for k, v in sorted(neighbors.items(), key=lambda item: item[1])}
        mrv = list(sorted_neighbors.keys())

        largest = sorted_neighbors[mrv[-1]]
        best = list()
        for var in mrv:
            if sorted_neighbors[var] == largest:
                best.append(var)

        return best[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if len(assignment) == len(self.crossword.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment.update({var: word})
            if self.consistent(new_assignment):
                assignment = new_assignment
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
