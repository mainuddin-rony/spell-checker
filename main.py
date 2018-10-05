import spelling_checker as checker
import os

# /home/rony/Work/Study/Fall 2018/NLP/Assignment 2/input.txt

def main_func():
    input_file = input("Enter the file path of the input:")
    if os.path.exists(input_file):
        with open(input_file, 'r') as fl:
            lines = fl.readlines()
            fl.close()

        output_line = " ".join(checker.process_input_lines(lines))
        with open('output.txt', 'w') as fl:
            fl.write(output_line)
            fl.close()
    else:
        print("Provide a valid file path")
        main_func()


if __name__ == "__main__":
    main_func()