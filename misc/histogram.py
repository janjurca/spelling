import matplotlib.pyplot as plt
import sys

def plot_histogram(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    lines = list(filter(lambda x: len(x) <= 512 and len(x) > 4 , lines))
    line_lengths = [len(line) for line in lines]
    print(max(line_lengths))
    print(min(line_lengths))

    plt.hist(line_lengths, bins='auto')
    plt.title('Histogram of line lengths')
    plt.xlabel('Line Length')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_name>")
    else:
        file_name = sys.argv[1]
        plot_histogram(file_name)
