import subprocess
import os

def calculate_mean(filename):
    try:
        with open(filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
        
        # Convert lines to a list of numbers, removing any empty lines or spaces
        numbers = [float(line.strip()) for line in lines if line.strip()]
        
        if not numbers:
            print("No numbers found in the file.")
            return
        
        # Calculate the mean of the numbers
        mean_value = sum(numbers) / len(numbers)
        
        # Print the mean value
        print(f"Mean: {mean_value}")
        print(f"Min: {min(numbers)}")
        print(f"Max: {max(numbers)}")

    except FileNotFoundError:
        print(f"File {filename} not found.")
    except ValueError:
        print("Some lines in the file are not valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")


LIM = 1000
for i in range(LIM):
    subprocess.run(
        [
            "python3",
            "generate_moves.py",
            "100",
        ]
    )
    os.system('clear')
    print(f'{i*100/LIM}%')
    


calculate_mean('mean.txt')
os.remove("mean.txt")
