import os


def convert_and_rename(input_file_path, output_filename):
    """
    Converts text to lowercase and saves with new filename in same directory

    Args:
        input_file_path (str): Full path to input text file
        output_filename (str): New filename (without path, include .txt extension)
    """
    # Get directory from input path
    directory = os.path.dirname(input_file_path)

    # Create full output path
    output_path = os.path.join(directory, output_filename)

    try:
        # Read and convert content
        with open(input_file_path, 'r', encoding='utf-8') as f_in:
            content = f_in.read().lower()

        # Write to new file
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(content)

        print(f"Successfully created: {output_path}")

    except Exception as e:
        print(f"Error processing file: {str(e)}")


# Example usage for your specific file:
input_file = r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche_nahmen.txt"
output_file = "test112.txt"
convert_and_rename(input_file, output_file)