from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # rule
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # game
    Or(
        And(AKnight, And(AKnight, AKnave)),
        And(AKnave, Not(And(AKnight, AKnave)))
    )
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # rule
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # game
    Or(
        And(AKnight, And(AKnave, BKnave)),
        And(AKnave, Not(And(AKnave, BKnave)))
    )
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # rule
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # game
    Or(
        And(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
        And(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))))
    ),

    Or(
        And(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
        And(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

knowledge3 = And(
    # TODO
# rule
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # game
    Or(
        And(AKnight, Or(AKnight, AKnave)),
        And(AKnave, Not(Or(AKnight, AKnave)))
    ),

    Or(
        And(BKnight, Or(And(AKnight, AKnave), And(AKnave, Not(AKnave)))),
        And(BKnave, Not(Or(And(AKnight, AKnave), And(AKnave, Not(AKnave)))))
    ),

    Or(
        And(BKnight, CKnave),
        And(BKnave, CKnight)
    ),

    Or(
        And(CKnight, AKnight),
        And(CKnave, AKnave)
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
