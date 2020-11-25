import sys

n = 3
N = n**2

def has_duplicates(l):
    return len(set(l)) < len(l)

class Sudoku:

    def __init__(self, given_numbers):
        self.given_numbers = given_numbers
        self.filled_numbers = [0 for _ in range(N**2 + 1)]
        for i in self.given_numbers.keys():
            self.filled_numbers[i] = self.given_numbers[i]
        self.p = 0
        self.o = 0


    def fill_next_number(self, number):
        self.filled_numbers[self.p] = number
        # jump over given numbers
        i = 1
        while(self.p + i in self.given_numbers.keys()):
            i = i + 1
        self.p = self.p + i
        # print("moved pointer to %i" % self.p)
        self.o = 0


    def delete_last_filled_number(self):
        self.filled_numbers[self.p] = 0
        i = 1
        while(self.p - i in self.given_numbers.keys()):
            i = i + 1
        self.p = self.p - i
        # print("moved pointer to %i" % self.p)
        self.o = self.filled_numbers[self.p]


    def is_solved(self):
        return self.p == N**2 + 1


    def get_option_for_next_number(self):
        self.o = self.o + 1
        if self.o > 9:
            return None
        else:
            return self.o


    def print_entries(self):
        for row in range(N):
            if row % n == 0:
                print("----------------------")
            row_string = "|"
            for j in range(n):
                for i in range(N*row + n*j, N*row + n*(j+1)):
                    if self.filled_numbers[i] == 0:
                         row_string = row_string + "  "
                    else:
                        row_string = row_string + " {}".format(self.filled_numbers[i])
                row_string = row_string + ("|")

            print(row_string)
        print("----------------------")


    def row_violation(self, row):
        numbers_in_row = [self.filled_numbers[i] for i in range(N*row, N*(row+1)) if not self.filled_numbers[i] == 0]
        return has_duplicates(numbers_in_row)


    def col_violation(self, col):
        numbers_in_col = [self.filled_numbers[i] for i in range(col, N**2, N) if not self.filled_numbers[i] == 0]
        return has_duplicates(numbers_in_col)


    def get_numbers_in_box(self, i,j):
        numbers_in_box = []
        for k in range(n):
            for l in range(n):
                number = self.filled_numbers[l + n*i + (n**2)*k + (n**3)*j]
                if not number == 0:
                    numbers_in_box.append(number)
        return numbers_in_box


    def box_violation(self, i,j):
        numbers_in_box = self.get_numbers_in_box(i,j)
        return has_duplicates(numbers_in_box)


    def violates_constraints(self):
        for i in range(N):
            if self.row_violation(i):
                return True
            if self.col_violation(i):
                return True
        for i in range(n):
            for j in range(n):
                if self.box_violation(i, j):
                    return True
        return False

    def solve(self):
        while(True):
            o = self.get_option_for_next_number()
            if o is None:
                self.delete_last_filled_number()
            else:
                self.fill_next_number(o)
                if self.violates_constraints():
                    # print(sudoku.p)
                    self.delete_last_filled_number()
                else:
                    if self.is_solved():
                        break

if __name__ == "__main__":

    unsolved = \
    [\
    0,2,0,0,0,4,3,0,0,\
    9,0,0,0,2,0,0,0,8,\
    0,0,0,6,0,9,0,5,0,\
    0,0,0,0,0,0,0,0,1,\
    0,7,2,5,0,3,6,8,0,\
    6,0,0,0,0,0,0,0,0,\
    0,8,0,2,0,5,0,0,0,\
    1,0,0,0,9,0,0,0,3,\
    0,0,9,8,0,0,0,6,0]

    given_numbers = dict()
    for i,number in enumerate(unsolved):
        if not number==0:
           given_numbers[i] = number

    sudoku = Sudoku(given_numbers)
    sudoku.print_entries()
    sudoku.solve()
    sudoku.print_entries()
