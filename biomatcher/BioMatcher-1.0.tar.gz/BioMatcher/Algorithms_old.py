from Bio import SeqIO
import py2exe


# Main function of comparison of the strings passed in input
def maincomparison(str1, str2):
    # Variable used as the counter of the while loop
    i = 0
    # Variable used as the counter of the equal letters inside the if of the while
    count = 0
    # If the lenght of the strings is different from each other or equal to 0, the function returns False
    if len(str1) != len(str2) or len(str1) == 0 or len(str2) == 0:
        return False

    while i < len(str1):
        if str1[i] == str2[i]:
            count += 1
        i += 1

    # The function return True if and only if all the letters of 2 strings have a length equal to the var cont
    return count == len(str1)


# Function that regards the comparison between seed 2-8 both human and vegetable
def compar28(str1, str2):
    return maincomparison(str1[1:8], str2[1:8])


# Function that regards the comparison between seed 2-7 both human and vegetable
def compar27(str1, str2):
    return maincomparison(str1[1:7], str2[1:7])


# Function that regards the comparison between seed 3-8 both human and vegetable
def compar38(str1, str2):
    return maincomparison(str1[2:8], str2[2:8])


# Function that regards the comparison between seed 2-7 human with 3-8 vegetable seed
def comparsl27(str1, str2):
    return maincomparison(str1[1:7], str2[2:8])


# Function that regards the comparison between seed 3-8 human with 2-7 vegetable seed
def comparsl38(str1, str2):
    return maincomparison(str1[2:8], str2[1:7])


# Function that calls all the functions that are part of the standard comparisons
# In this case, all the functions called up must return True so that this function return True
def comparisonsstandard(str1, str2):
    return compar28(str1, str2) and compar27(str1, str2) and compar38(str1, str2) and comparsl27(str1, str2) and comparsl38(
        str1, str2)


# Function that calls all the functions that are part of the standard comparisons
# In this case, as long as just a single function returns True so that this function return True
def atleastonecomparisonstandard(str1, str2):
    return compar28(str1, str2) or compar27(str1, str2) or compar38(str1, str2) or comparsl27(str1, str2) or comparsl38(
        str1, str2)


def main():

    # DA INSERIRE IN TESTS?

    # Final test with reduced files
    # I tried to look for the identical sequences within these 2 reduced files through the use of the 2 summary functions
    #   "comparisonsstandard" and "atleastonecomparisonstandard".
    # In the first case it is very difficult to find a sequence that satisfies this function.
    # For the second case, on the other hand, 259 sequences were found that satisfy the "atleastonecomparisonstandard" function.
    print("----Final Test----")

    same_seq_firstfoo = 0
    same_seq_secondfoo = 0
    for seq_human in SeqIO.parse("mature_human_reduced.fa", "fasta"):
        for seq_plant in SeqIO.parse("mature_plant_reduced.fa", "fasta"):
            if comparisonsstandard(seq_human.seq, seq_plant):
                same_seq_firstfoo += 1
            if atleastonecomparisonstandard(seq_human.seq, seq_plant):
                same_seq_secondfoo += 1

    print(f"The sequences that satisfy the 'comparisonsstandard' function are {same_seq_firstfoo}")
    print(f"The sequences that satisfy the 'atleastonecomparisonstandard' function are {same_seq_secondfoo}")

    # Ho commentato perché richiede un elevato tempo di esecuzione

    # same_seq = 0
    # for seq_human in SeqIO.parse("mature_human.fa", "fasta"):
    #     for seq_plant in SeqIO.parse("mature_plant.fa", "fasta"):
    #         if comparisonsstandard(seq_human.seq, seq_plant):
    #             print(seq_human.description.split(' ')[1] + " + " + seq_plant.description.split('|')[1])
    #             same_seq += 1
    #
    # print(same_seq)


if __name__ == '__main__':
    main()
